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
