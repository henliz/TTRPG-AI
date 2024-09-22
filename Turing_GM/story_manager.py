from pdf_handler import PDFStoryHandler

class StoryManager:
    def __init__(self, game_system):
        self.game_system = game_system
        if game_system.lower() == "d&d 5e":
            self.curse_of_strahd = CurseOfStrahd()

    def generate_response(self, prompt, mode=None):
        if self.game_system.lower() == "d&d 5e":
            return self.curse_of_strahd.generate_response(prompt)
        return "I'm not equipped to handle that game system."


class CurseOfStrahd:
    def __init__(self):
        pdf_path = r"C:\Users\Henrietta\PycharmProjects\TTRPG-AI\Campaigns\DnD\curse_of_strahd.pdf"
        self.pdf_handler = PDFStoryHandler(pdf_path)

    def generate_response(self, prompt):
        if any(word in prompt.lower() for word in ["strahd", "barovia", "item"]):
            section = self.pdf_handler.search(prompt)
            if section:
                return f"Here are some items you might find: {section[:500]}"
            else:
                return "I couldn't find any specific information on that."
        return "I don't have that information in my current system."
