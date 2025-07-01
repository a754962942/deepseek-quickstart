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
