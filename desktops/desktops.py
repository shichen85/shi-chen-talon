import re
from difflib import SequenceMatcher

from talon import Context, Module, actions, ui

mod = Module()
desktop_max_setting = mod.setting(
    "desktop_count_max",
    type=int,
    default=4,
    desc="Windows does not have hotkeys to go to specific desktops, so we need a hack based on the total number of desktops. This number must be >= the number of desktops in your setup.",
)

ctx = Context()
ctx.matches = r"""
os: windows
"""


@mod.action_class
class Actions:
    def focus_app_by_title(app_name: str, title_search: str) -> None:
        """Focus application by title, with a search"""


@ctx.action_class("user")
class Actions:
    def desktop(number: int):
        # Go all the way left
        for i in range(desktop_max_setting.get()):
            actions.key("ctrl-win-left")
        if number > 1:
            for i in range(1, number):
                actions.key("ctrl-win-right")

    def focus_app_by_title(app_name: str, title_search: str) -> None:
        # See which app it is using knausj behavior
        # (throws if none found)
        matching_app: ui.App = actions.user.get_running_app(app_name)

        # Get the windows associated with the app
        windows = matching_app.windows()

        # Default to knausj behavior if no title provided
        # or no choicese to be made
        if not title_search or len(windows) < 2:
            return actions.user.switcher_focus_app(matching_app)

        # Find the window with the closest title match
        scored_windows = []
        for window in windows:
            window.title
            score = _phrase_match_score(window.title, title_search)
            scored_windows.append((score, window))

        scored_windows.sort(key=lambda x: x[0], reverse=True)
        return actions.user.switcher_focus_window(scored_windows[0][1])


def _string_to_normalized_words(string: str) -> list[str]:
    """
    Convert a string to a normalized collection of
    "words". Breaks on spaces, punctuation, and
    lower-to-upper case changes. All words are forced
    lower case.
    """
    clean = re.sub(r'[^a-zA-Z0-9]+', ' ', string)
    # Wherever a lowercase bumps against an uppercase, split there too
    clean = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', clean)
    # Wherever numbers bump against letters, split there too
    clean = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', clean)
    clean = re.sub(r'([0-9])([a-zA-Z])', r'\1 \2', clean)
    words = [word.lower() for word in re.split(r'\s+', clean.strip()) if word]
    return words


def _word_match_score(word1: str, word2: str) -> int:
    """
    Score a word match. Max is 1 (perfect match) and
    min is 0 (very dissimilar). Intent is to reflect
    similarity in how the words *sound*, but don't want
    to do a lot of heavy lifting or rely on 3rd party
    libraries. Expect scores to change with updates!
    """
    if(not word1 or not word2):
        return 0
    if word1 == word2:
        return 1
    return SequenceMatcher(None, word1, word2).ratio()


def _phrase_match_score(phrase1: str, phrase2: str) -> int:
    """
    Score a phrase match, assuming order of words does not
    matter. Expect scores to change with updates!
    """
    if(not phrase1 or not phrase2):
        return 0
    words1 = _string_to_normalized_words(phrase1)
    words2 = _string_to_normalized_words(phrase2)
    if(not words1 or not words2):
        return 0
    score = 0
    for word1 in words1:
        best_score = 0
        for word2 in words2:
            best_score = max(best_score, _word_match_score(word1, word2))
        score += best_score
    return score
