#!/bin/bash

# 创建项目目录结构
mkdir deepseek-frontend
cd deepseek-frontend
npm init vite@latest . -- --template react
mkdir -p src/{components,pages}
mkdir -p public

# 创建前端文件
cat > src/main.jsx << 'EOL'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
EOL

cat > src/App.jsx << 'EOL'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Products from './pages/Products'
import Developers from './pages/Developers'
import Solutions from './pages/Solutions'
import Resources from './pages/Resources'
import About from './pages/About'

const { Header, Content, Footer } = Layout

function App() {
  return (
    <Router>
      <Layout className="layout">
        <Header>
          <Navbar />
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/products" element={<Products />} />
            <Route path="/developers" element={<Developers />} />
            <Route path="/solutions" element={<Solutions />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </Content>
        <Footer style={{ textAlign: 'center' }}>
          DeepSeek AI ©2023
        </Footer>
      </Layout>
    </Router>
  )
}

export default App
EOL

cat > src/components/Navbar.jsx << 'EOL'
import { Menu } from 'antd'
import { Link } from 'react-router-dom'
import { HomeOutlined, AppstoreOutlined, CodeOutlined, SolutionOutlined, BookOutlined, TeamOutlined } from '@ant-design/icons'

const items = [
  {
    label: <Link to="/">Home</Link>,
    key: 'home',
    icon: <HomeOutlined />
  },
  {
    label: <Link to="/products">Products</Link>,
    key: 'products',
    icon: <AppstoreOutlined />
  },
  {
    label: <Link to="/developers">Developers</Link>,
    key: 'developers',
    icon: <CodeOutlined />
  },
  {
    label: <Link to="/solutions">Solutions</Link>,
    key: 'solutions',
    icon: <SolutionOutlined />
  },
  {
    label: <Link to="/resources">Resources</Link>,
    key: 'resources',
    icon: <BookOutlined />
  },
  {
    label: <Link to="/about">About</Link>,
    key: 'about',
    icon: <TeamOutlined />
  }
]

function Navbar() {
  return <Menu theme="dark" mode="horizontal" items={items} />
}

export default Navbar
EOL

cat > src/pages/Home.jsx << 'EOL'
import { Carousel, Card, Row, Col, Button } from 'antd'
import { RocketOutlined, BulbOutlined, ApiOutlined } from '@ant-design/icons'

const contentStyle = {
  height: '400px',
  color: '#fff',
  lineHeight: '400px',
  textAlign: 'center',
  background: '#1E88E5'
}

function Home() {
  return (
    <div>
      <Carousel autoplay>
        <div>
          <h3 style={contentStyle}>Powerful AI Models</h3>
        </div>
        <div>
          <h3 style={contentStyle}>Easy-to-use APIs</h3>
        </div>
        <div>
          <h3 style={contentStyle}>Industry Solutions</h3>
        </div>
      </Carousel>

      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={8}>
          <Card title="Language Models" bordered={false}>
            <p><RocketOutlined /> State-of-the-art NLP</p>
            <Button type="primary">Learn More</Button>
          </Card>
        </Col>
        <Col span={8}>
          <Card title="Computer Vision" bordered={false}>
            <p><BulbOutlined /> Advanced image analysis</p>
            <Button type="primary">Learn More</Button>
          </Card>
        </Col>
        <Col span={8}>
          <Card title="API Access" bordered={false}>
            <p><ApiOutlined /> Developer friendly</p>
            <Button type="primary">Get Started</Button>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Home
EOL

# 创建空页面组件
for page in Products Developers Solutions Resources About; do
  cat > src/pages/${page}.jsx << 'EOL'
import { Card } from 'antd'

function ${page}() {
  return (
    <Card title="${page}">
      <p>${page} page content coming soon</p>
    </Card>
  )
}

export default ${page}
EOL
done

# 创建后端API文件
cat > main.py << 'EOL'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DeepSeek API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to DeepSeek API"}

@app.get("/products")
async def get_products():
    return [
        {"id": 1, "name": "Language Model", "category": "NLP"},
        {"id": 2, "name": "Computer Vision", "category": "CV"},
        {"id": 3, "name": "Speech Recognition", "category": "ASR"}
    ]

@app.get("/docs")
async def get_docs():
    return [
        {"id": 1, "title": "API Reference", "type": "documentation"},
        {"id": 2, "title": "Quick Start", "type": "tutorial"}
    ]
EOL

# 初始化前端项目并安装依赖

npm install antd react-router-dom axios @ant-design/icons
cd ..

# 安装后端依赖
pip3 install fastapi uvicorn sqlalchemy pymysql python-jose[cryptography] passlib[bcrypt]

echo "项目创建完成！"
echo "前端运行: cd deepseek-frontend && npm run dev"
echo "后端运行: uvicorn main:app --reload"
