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
