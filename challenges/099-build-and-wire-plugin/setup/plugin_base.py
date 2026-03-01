from abc import ABC, abstractmethod

class Plugin(ABC):
    """Base class for all plugins."""

    @abstractmethod
    def name(self):
        """Return the plugin name."""
        pass

    @abstractmethod
    def transform(self, text):
        """Transform the input text."""
        pass

    def configure(self, settings):
        """Optional configuration. Override if needed."""
        self.settings = settings
