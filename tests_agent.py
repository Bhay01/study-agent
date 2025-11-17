import unittest

# --- Mock Implementation of the StudyAgent Class ---
class StudyAgent:
    """
    A hypothetical agent designed to simulate loading material, studying,
    and tracking a knowledge level.
    """
    def __init__(self, name="Study Agent", initial_state="idle", knowledge_level=0):
        self.name = name
        self.state = initial_state
        self.knowledge_level = knowledge_level # A score from 0 to 100
        self.loaded_material = None
        self.memory = []

    def load_material(self, topic: str):
        """Loads a topic and prepares the agent for study."""
        self.loaded_material = topic
        self.state = "ready to study"
        self.log_event(f"Loaded material: {topic}")
        return f"{self.name} is now prepared to study {topic}."

    def study(self, duration_minutes: int):
        """
        Simulates the act of studying, increasing the knowledge level based on duration.
        Knowledge gain is capped at 100.
        """
        if not self.loaded_material:
            self.state = "idle"
            return f"{self.name} has no material loaded to study."

        self.state = "studying"
        # Simulate knowledge gain (1 point per 5 minutes of study)
        gain = duration_minutes // 5
        self.knowledge_level = min(100, self.knowledge_level + gain)
        self.state = "ready for test"
        self.log_event(f"Studied for {duration_minutes} mins. Knowledge now {self.knowledge_level}.")
        return f"{self.name} finished studying. Knowledge level: {self.knowledge_level}%."

    def check_knowledge(self, required_level=50) -> bool:
        """Checks if the current knowledge level meets a required threshold."""
        self.state = "testing"
        is_sufficient = self.knowledge_level >= required_level
        self.state = "idle"
        return is_sufficient

    def log_event(self, event):
        """Adds an event to the agent's memory."""
        self.memory.append(event)
        return True
# --- End of Mock Implementation ---

class TestStudyAgent(unittest.TestCase):
    """
    Test suite for the StudyAgent class.
    """

    def setUp(self):
        """
        Creates a fresh StudyAgent instance for each test, starting with low knowledge.
        """
        # Start the agent with 10% base knowledge
        self.agent = StudyAgent(name="LearningBot", initial_state="idle", knowledge_level=10)
        # print(f"\nSetting up LearningBot: {self.agent.name}") # Suppressing print for cleaner test output

    def test_initialization_and_base_knowledge(self):
        """
        Tests if the StudyAgent is initialized correctly, including the knowledge level.
        """
        self.assertEqual(self.agent.name, "LearningBot")
        self.assertEqual(self.agent.state, "idle")
        self.assertEqual(self.agent.knowledge_level, 10)
        self.assertIsInstance(self.agent.memory, list)

    def test_load_material_transition(self):
        """
        Tests the transition to 'ready to study' state and material loading.
        """
        result = self.agent.load_material("Quantum Physics")
        self.assertEqual(self.agent.state, "ready to study")
        self.assertEqual(self.agent.loaded_material, "Quantum Physics")
        self.assertIn("prepared to study Quantum Physics", result)

    def test_study_knowledge_gain(self):
        """
        Tests if studying increases the knowledge level and updates state.
        """
        self.agent.load_material("History of Python")
        initial_knowledge = self.agent.knowledge_level # 10
        
        # 30 minutes of study should increase knowledge by 30 // 5 = 6 points
        duration = 30
        result = self.agent.study(duration)
        
        expected_knowledge = initial_knowledge + (duration // 5)
        self.assertEqual(self.agent.knowledge_level, expected_knowledge) # 10 + 6 = 16
        self.assertEqual(self.agent.state, "ready for test")
        self.assertIn("finished studying", result)

    def test_study_without_material_failure(self):
        """
        Tests the defensive behavior when study is called without loaded material.
        """
        initial_knowledge = self.agent.knowledge_level
        result = self.agent.study(60)
        
        self.assertEqual(self.agent.knowledge_level, initial_knowledge) # Knowledge should not change
        self.assertEqual(self.agent.state, "idle") # Should return to idle
        self.assertIn("has no material loaded", result)

    def test_knowledge_check_pass(self):
        """
        Tests if check_knowledge returns True when the level is sufficient.
        """
        # Manually boost knowledge to ensure passing
        self.agent.knowledge_level = 75
        is_pass = self.agent.check_knowledge(required_level=50)

        self.assertTrue(is_pass)
        self.assertEqual(self.agent.state, "idle")

    def test_knowledge_check_fail(self):
        """
        Tests if check_knowledge returns False when the level is insufficient.
        """
        # Agent starts at 10, which is insufficient for 50
        is_pass = self.agent.check_knowledge(required_level=50)

        self.assertFalse(is_pass)
        self.assertEqual(self.agent.state, "idle")

    def test_knowledge_cap(self):
        """
        Tests that the knowledge level cannot exceed 100.
        """
        self.agent.load_material("Everything")
        self.agent.knowledge_level = 90
        # Study for 60 minutes, which should add 12 points (90+12 = 102)
        self.agent.study(60)
        self.assertEqual(self.agent.knowledge_level, 100) # Should be capped at 100

    def tearDown(self):
        """
        Clean up method called after every test function.
        """
        self.agent = None


if __name__ == '__main__':
    # Runs the test suite when the file is executed directly
    unittest.main()
