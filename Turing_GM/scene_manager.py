class SceneManager:
    def __init__(self, game_system):
        self.game_system = game_system

    def get_scene_description(self, location, npcs=[]):
        if self.game_system == "D&D 5e":
            return self.dnd_scene(location, npcs)
        elif self.game_system == "Cyberpunk RED":
            return self.cyberpunk_scene(location, npcs)

    def dnd_scene(self, location, npcs):
        # Custom description for D&D scenes
        return f"In the heart of {location}, you see {', '.join(npcs)} lurking around."

    def cyberpunk_scene(self, location, npcs):
        # Custom description for Cyberpunk scenes
        return f"{location} is a sprawling urban jungle, with neon lights flickering as {', '.join(npcs)} pass by."
