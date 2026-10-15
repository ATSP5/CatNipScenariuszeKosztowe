import glob
import os


class ProjectFolders:
    """Folder projektu (ten z plikiem .catnip) i jego podfoldery: input/ na dane, output/ na wyniki.

    Działa tak samo lokalnie i w Dockerze (/app), bo szuka pliku .catnip, a nie ścieżki z dysku C:.
    """

    def __init__(self, input_name: str = "input", output_name: str = "output"):
        self.root = self.find_root()
        self.input_dir = os.path.join(self.root, input_name)
        self.output_dir = os.path.join(self.root, output_name)
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def folders(self) -> "ProjectFolders":
        return self

    @staticmethod
    def find_root() -> str:
        for folder in (os.getcwd(), os.path.dirname(os.path.abspath(__file__))):
            if glob.glob(os.path.join(folder, "*.catnip")):
                return folder
        return os.getcwd()

    def input_path(self, file_name: str) -> str:
        return os.path.join(self.input_dir, file_name)

    def output_path(self, file_name: str) -> str:
        return os.path.join(self.output_dir, file_name)
