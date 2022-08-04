from talon import noise, actions

def on_hiss(active):
    actions.speech.disable();
noise.register("hiss", on_hiss)

def on_pop(active):
    print("pop");    
    actions.speech.enable();
noise.register("pop", on_pop)