class CurseOfStrahd:
    def __init__(self):
        self.current_chapter = 1  # Start at the beginning of the story

    def get_response(self, prompt, mode):
        # This would be based on your chapter and what part of the story you're in
        if mode == "descriptive":
            return self.describe_scene(prompt)
        else:
            return self.general_response(prompt)

    def describe_scene(self, prompt):
        # Return a description of the current scene based on the chapter
        return f"You're in Chapter {self.current_chapter}. {self.get_current_scene_description()}"

    def general_response(self, prompt):
        # Return a general conversation response
        return f"Strahd says: {prompt}"

    def get_current_scene_description(self):
        if self.current_chapter == 1:
            return "The mists surround Barovia, an eerie fog blankets the ground..."
        elif self.current_chapter == 2:
            return "You find yourself in the village of Barovia..."
        else:
            return "The adventure continues..."
