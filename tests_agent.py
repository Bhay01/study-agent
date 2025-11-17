import unittest

# --- Mock Implementation of the Agent Class (for demonstration) ---
# In a real project, you would replace this with:
# from your_project.agent import Agent

class Agent:
    """
    A simple, hypothetical agent class with basic functionalities.
    """
    def __init__(self, name="Default Agent", initial_state="idle"):
        self.name = name
        self.state = initial_state
        self.memory = []

    def perform_action(self, action_type):
        """Changes the agent's state based on the action."""
        if action_type == "work":
            self.state = "working"
            return f"{self.name} started working."
        elif action_type == "rest":
            self.state = "resting"
            return f"{self.name} is now resting."
        else:
            return f"{self.name} performed an unknown action."

    def log_event(self, event):
        """Adds an event to the agent's memory."""
        self.memory.append(event)
        return True
# --- End of Mock Implementation ---

class TestAgent(unittest.TestCase):
    """
    Test suite for the Agent class using Python's unittest framework.
    """

    def setUp(self):
        """
        Set up method called before every test function.
        It creates a fresh Agent instance for each test.
        """
        self.agent = Agent(name="TestAgent", initial_state="ready")
        print(f"\nSetting up TestAgent: {self.agent.name}")

    def test_initialization(self):
        """
        Tests if the Agent is initialized correctly with name and state.
        """
        print("Testing: Initialization")
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(self.agent.state, "ready")
        self.assertIsInstance(self.agent.memory, list)
        self.assertFalse(self.agent.memory) # Check if memory is empty

    def test_perform_work_action(self):
        """
        Tests the transition to the 'working' state.
        """
        print("Testing: Perform Work Action")
        result = self.agent.perform_action("work")
        self.assertEqual(self.agent.state, "working")
        self.assertIn("started working", result)

    def test_perform_rest_action(self):
        """
        Tests the transition to the 'resting' state.
        """
        print("Testing: Perform Rest Action")
        result = self.agent.perform_action("rest")
        self.assertEqual(self.agent.state, "resting")
        self.assertIn("now resting", result)

    def test_perform_unknown_action(self):
        """
        Tests the response for an action that is not defined.
        The state should remain unchanged ('ready').
        """
        print("Testing: Perform Unknown Action")
        initial_state = self.agent.state
        result = self.agent.perform_action("think_deeply")
        self.assertEqual(self.agent.state, initial_state) # State should not change
        self.assertIn("unknown action", result)

    def test_log_event(self):
        """
        Tests logging an event and verifies it is added to the memory list.
        """
        print("Testing: Log Event")
        event = "Model trained successfully."
        self.agent.log_event(event)
        self.assertEqual(len(self.agent.memory), 1)
        self.assertIn(event, self.agent.memory)

    def tearDown(self):
        """
        Clean up method called after every test function.
        """
        # In this simple example, cleanup is minimal, but could include
        # closing database connections, deleting temporary files, etc.
        self.agent = None
        print(f"Tearing down TestAgent.")


if __name__ == '__main__':
    # Runs the test suite when the file is executed directly
    print("--- Starting Agent Test Suite ---")
    unittest.main()
