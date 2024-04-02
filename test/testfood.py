import unittest
from unittest.mock import Mock
from food import Food

class TestSnakeFood(unittest.TestCase):
    def test_init(self):
        # Test initialization of Food class
        size = 20
        boundary = (800, 600)
        food = Food(size, boundary)

        self.assertEqual(food.size, size)
        self.assertEqual(food.boundary, boundary)

        self.assertTrue(0 <= food.x < boundary[0])
        self.assertTrue(0 <= food.y < boundary[1])

    def test_draw(self):
        # Simulate instance of Food
        size = 20
        boundary = (800, 600)
        food = Food(size, boundary)
        food.x = 40
        food.y = 60
        mock_win = Mock()

        draw_rect_mock = Mock()
        game_mock = Mock()
        game_mock.draw.rect = draw_rect_mock

        food.draw(game_mock, mock_win)

        draw_rect_mock.assert_called_once_with(mock_win, food.color, (food.x, food.y, size, size))
    def test_respawn(self):
        # Test respawn method
        size = 20
        boundary = (800, 600)
        food = Food(size, boundary)

        initial_x = food.x
        initial_y = food.y

        food.respawn()

        self.assertNotEqual(food.x, initial_x)
        self.assertNotEqual(food.y, initial_y)