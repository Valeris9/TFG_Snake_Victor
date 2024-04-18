import pygame
import unittest
from unittest.mock import Mock, call
from game import Snake, Direction


class TestSnakeGame(unittest.TestCase):
    def test_snake_init(self):
        # Test if the snake is initialized correctly
        block_size = 20
        boundary = (800, 600)
        snake = Snake(block_size, boundary)
        self.assertEqual(snake.length, 2)
        self.assertEqual(snake.direction, Direction.RIGHT)
        self.assertEqual(len(snake.body), 3)
        self.assertEqual(snake.block_size, block_size)
        self.assertEqual(snake.boundary, boundary)

    def test_update_score(self):
        snake = Snake(20, (800, 600))
        initial_score = snake.score
        snake.update_score()
        self.assertEqual(snake.score, initial_score + 1)
    def test_snake_steer(self):
        # Test if the snake can steer correctly
        block_size = 20
        boundary = (800, 600)
        snake = Snake(block_size, boundary)
        snake.steer(Direction.RIGHT)
        snake.move()
        self.assertEqual(snake.body[-1], (40, 60)) # Snake moves right
        snake.steer(Direction.UP)
        snake.move()
        self.assertEqual(snake.body[-1], (40, 40))
        snake.steer(Direction.LEFT)
        snake.move()
        self.assertEqual(snake.body[-1], (20, 40))
        snake.steer(Direction.DOWN)
        snake.move()
        self.assertEqual(snake.body[-1], (20, 60))


    def test_snake_move(self):
        # Test if the snake can move correctly
        block_size = 20
        boundary = (800, 600)
        snake = Snake(block_size, boundary)
        snake.move()
        self.assertEqual(snake.body[-1], (40, 60))
        snake.move()
        self.assertEqual(snake.body[-1], (60, 60))
        snake.move()
        self.assertEqual(snake.body[-1], (80, 60))

    def test_snake_draw(self):
        #Simulate instance of Snake
        block_size = 20
        boundary = (800, 600)
        snake = Snake(block_size, boundary)
        snake.body = [(20, 20), (20, 40), (20, 60)]

        #Mock the window
        mock_win = Mock(spec=pygame.Surface)

        #Mock pygame.draw.rect
        draw_rect_mock = Mock()
        pygame.draw.rect = draw_rect_mock

        #Draw
        snake.draw(pygame, mock_win)

        expected_calls = [call(mock_win, (0, 255, 0), (20, 20, 20, 20)),
                          call(mock_win, (0, 255, 0), (20, 40, 20, 20)),
                          call(mock_win, (0, 255, 0), (20, 60, 20, 20))]

        actual_calls = draw_rect_mock.call_args_list
        self.assertEqual(actual_calls, expected_calls)

    def test_check_collision_food(self):
        #Simulate instance of Snake and Food
        block_size = 20
        boundary = (800, 600)
        snake = Snake(block_size, boundary)
        snake.body = [(20, 20), (20, 40), (20, 60)]
        food = Mock()
        food.x = 20
        food.y = 60

        snake.eat = Mock()
        food.respawn = Mock()

        snake.check_collision_food(food)
        snake.eat.assert_called_once()
        food.respawn.assert_called_once()

    def test_eat(self):
            # Simulate instance of Snake
            block_size = 20
            boundary = (800, 600)
            snake = Snake(block_size, boundary)
            initial_length = snake.length
            initial_score = snake.score
            snake.body = [(20, 20), (20, 40), (20, 60)]
            snake.eat()
            self.assertEqual(snake.length, initial_length + 1)
            self.assertEqual(snake.score, initial_score + 1)

    def test_check_collision_tail(self):
        #Simulate instance of Snake
        block_size = 20
        boundary = (800, 600)
        snake = Snake(block_size, boundary)
        snake.body = [(20, 20), (20, 40), (20, 60)]
        self.assertFalse(snake.check_collision_tail())
        snake.body.append((20, 60))
        self.assertTrue(snake.check_collision_tail())

    def test_check_collision_boundary(self):
        #Simulate instance of Snake
        block_size = 20
        boundary = (800, 600)
        snake = Snake(block_size, boundary)
        snake.body = [(20, 20), (20, 40), (20, 60)]
        self.assertFalse(snake.check_collision_boundary())
        snake.body.append((800, 60))
        self.assertTrue(snake.check_collision_boundary())