#!/bin/bash

# Create directory structure
mkdir -p src

# Create and write App.jsx
cat > src/App.jsx << 'EOL'
import { useEffect, useRef, useState } from 'react';
import './App.css';

function App() {
  const canvasRef = useRef(null);
  const [score, setScore] = useState(0);
  const [highScore, setHighScore] = useState(0);
  const [gameStatus, setGameStatus] = useState('running');
  
  const GRID_SIZE = 20;
  const GRID_COUNT = 20;
  const gameState = useRef({
    snake: [],
    food: {},
    direction: 'right',
    nextDirection: 'right',
    gameSpeed: 150,
    gameInterval: null
  });

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Initialize game
    initGame(ctx);
    
    // Load high score from localStorage
    const savedHighScore = localStorage.getItem('snakeHighScore') || 0;
    setHighScore(parseInt(savedHighScore));

    // Set up keyboard controls
    const handleKeyDown = (e) => {
      const { direction } = gameState.current;
      
      switch (e.key) {
        case 'ArrowUp':
          if (direction !== 'down') gameState.current.nextDirection = 'up';
          break;
        case 'ArrowDown':
          if (direction !== 'up') gameState.current.nextDirection = 'down';
          break;
        case 'ArrowLeft':
          if (direction !== 'right') gameState.current.nextDirection = 'left';
          break;
        case 'ArrowRight':
          if (direction !== 'left') gameState.current.nextDirection = 'right';
          break;
        case ' ':
          // Space to pause/resume
          if (gameStatus === 'running') {
            setGameStatus('paused');
            clearInterval(gameState.current.gameInterval);
          } else if (gameStatus === 'paused') {
            setGameStatus('running');
            gameState.current.gameInterval = setInterval(() => gameLoop(ctx), gameState.current.gameSpeed);
          }
          break;
        case 'r':
        case 'R':
          // R to restart
          if (gameStatus === 'gameover') {
            initGame(ctx);
            setGameStatus('running');
          }
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      clearInterval(gameState.current.gameInterval);
    };
  }, [gameStatus]);

  const initGame = (ctx) => {
    // Initialize snake
    gameState.current.snake = [
      {x: 5, y: 10},
      {x: 4, y: 10},
      {x: 3, y: 10}
    ];
    
    // Initialize direction
    gameState.current.direction = 'right';
    gameState.current.nextDirection = 'right';
    
    // Generate food
    generateFood();
    
    // Reset score
    setScore(0);
    
    // Clear previous game loop
    if (gameState.current.gameInterval) {
      clearInterval(gameState.current.gameInterval);
    }
    
    // Reset game speed
    gameState.current.gameSpeed = 150;
    
    // Start new game
    gameState.current.gameInterval = setInterval(() => gameLoop(ctx), gameState.current.gameSpeed);
    
    // Draw initial state
    draw(ctx);
  };

  const generateFood = () => {
    let validPosition = false;
    while (!validPosition) {
      gameState.current.food = {
        x: Math.floor(Math.random() * GRID_COUNT),
        y: Math.floor(Math.random() * GRID_COUNT)
      };
      
      validPosition = true;
      for (let segment of gameState.current.snake) {
        if (segment.x === gameState.current.food.x && segment.y === gameState.current.food.y) {
          validPosition = false;
          break;
        }
      }
    }
  };

  const gameLoop = (ctx) => {
    if (gameStatus !== 'running') return;
    
    moveSnake();
    checkCollision();
    draw(ctx);
  };

  const moveSnake = () => {
    const { snake, direction, nextDirection, food } = gameState.current;
    
    // Update direction
    gameState.current.direction = nextDirection;
    
    // Calculate new head position
    const head = {x: snake[0].x, y: snake[0].y};
    
    switch (direction) {
      case 'up':
        head.y -= 1;
        break;
      case 'down':
        head.y += 1;
        break;
      case 'left':
        head.x -= 1;
        break;
      case 'right':
        head.x += 1;
        break;
    }
    
    // Add new head to the beginning of the array
    gameState.current.snake.unshift(head);
    
    // Check if food was eaten
    if (head.x === food.x && head.y === food.y) {
      // Increase score
      const newScore = score + 10;
      setScore(newScore);
      
      // Speed up every 5 foods
      if (newScore % 50 === 0 && gameState.current.gameSpeed > 50) {
        gameState.current.gameSpeed -= 10;
        clearInterval(gameState.current.gameInterval);
        gameState.current.gameInterval = setInterval(() => gameLoop(canvasRef.current.getContext('2d')), gameState.current.gameSpeed);
      }
      
      // Generate new food
      generateFood();
    } else {
      // Remove tail if no food was eaten
      gameState.current.snake.pop();
    }
  };

  const checkCollision = () => {
    const { snake } = gameState.current;
    const head = snake[0];
    
    // Check wall collision
    if (head.x < 0 || head.x >= GRID_COUNT || head.y < 0 || head.y >= GRID_COUNT) {
      gameOver();
      return;
    }
    
    // Check self collision
    for (let i = 1; i < snake.length; i++) {
      if (head.x === snake[i].x && head.y === snake[i].y) {
        gameOver();
        return;
      }
    }
  };

  const gameOver = () => {
    setGameStatus('gameover');
    clearInterval(gameState.current.gameInterval);
    
    // Update high score
    if (score > highScore) {
      const newHighScore = score;
      setHighScore(newHighScore);
      localStorage.setItem('snakeHighScore', newHighScore.toString());
    }
  };

  const draw = (ctx) => {
    const { snake, food } = gameState.current;
    
    // Clear canvas
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    
    // Draw snake
    for (let i = 0; i < snake.length; i++) {
      ctx.fillStyle = i === 0 ? '#4CAF50' : '#8BC34A';
      ctx.fillRect(
        snake[i].x * GRID_SIZE,
        snake[i].y * GRID_SIZE,
        GRID_SIZE - 1,
        GRID_SIZE - 1
      );
    }
    
    // Draw food
    ctx.fillStyle = '#FF5722';
    ctx.fillRect(
      food.x * GRID_SIZE,
      food.y * GRID_SIZE,
      GRID_SIZE - 1,
      GRID_SIZE - 1
    );
    
    // Draw game over or paused state
    if (gameStatus === 'gameover') {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
      ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      ctx.fillStyle = 'white';
      ctx.font = '30px Arial';
      ctx.textAlign = 'center';
      ctx.fillText('游戏结束!', ctx.canvas.width/2, ctx.canvas.height/2 - 20);
      ctx.font = '20px Arial';
      ctx.fillText('按R键重新开始', ctx.canvas.width/2, ctx.canvas.height/2 + 20);
    } else if (gameStatus === 'paused') {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
      ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
      ctx.fillStyle = 'white';
      ctx.font = '30px Arial';
      ctx.textAlign = 'center';
      ctx.fillText('已暂停', ctx.canvas.width/2, ctx.canvas.height/2);
    }
  };

  return (
    <div className="game-container">
      <h1>贪吃蛇游戏</h1>
      <canvas
        ref={canvasRef}
        width={GRID_SIZE * GRID_COUNT}
        height={GRID_SIZE * GRID_COUNT}
      />
      <div className="score">分数: {score} | 最高分: {highScore}</div>
      <p>使用方向键控制，空格键暂停</p>
      {gameStatus === 'gameover' && <p>按R键重新开始</p>}
    </div>
  );
}

export default App;
EOL

# Create and write App.css
cat > src/App.css << 'EOL'
body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
  background-color: #f0f0f0;
  font-family: Arial, sans-serif;
}

.game-container {
  text-align: center;
}

canvas {
  border: 2px solid #333;
  background-color: #fff;
}

.score {
  margin-top: 10px;
  font-size: 20px;
}
EOL

# Create and write main.jsx
cat > src/main.jsx << 'EOL'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOL

# Create and write index.html
cat > index.html << 'EOL'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Canvas贪吃蛇</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOL

# Create empty index.css
touch src/index.css

# Install dependencies and run the app
npm create vite@latest snake-game -- --template react
cd snake-game
cp -r ./src ./snake-game
cp  ./index.html ./snake-game
npm install
npm run dev
