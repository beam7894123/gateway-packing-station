import React from 'react'
import { useNavigate } from 'react-router-dom';
import {
  CButton,
  CCarousel,
  CCarouselItem,
  CCol,
  CImage,
  CRow
} from '@coreui/react'


const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <>
    <h1 className="text-center pb-2">Welcome to PSG Admin panel! (Demo)</h1>
    <CRow>
      <CCol>
        <CButton color="primary" className="w-100" onClick={() => navigate(`/items`)} >Items list</CButton>
      </CCol>
      <CCol>
        <CButton color="primary" className="w-100" onClick={() => navigate(`/orders`)} >Orders list</CButton>
      </CCol>
      <CCol>
        <CButton color="primary" className="w-100" onClick={() => navigate(`/packing`)} >Packing rec</CButton>
      </CCol>
    </CRow>
      <CCarousel indicators animate autoPlay={3000} className='py-4'>
        <CCarouselItem>
          <CImage className="d-block w-100" src="../images/react.jpg" alt="slide 1" />
        </CCarouselItem>
        <CCarouselItem>
          <CImage className="d-block w-100" src="../images/vue.jpg" alt="slide 2" />
        </CCarouselItem>
        <CCarouselItem>
          <CImage className="d-block w-100" src="../images/angular.jpg" alt="slide 3" />
        </CCarouselItem>
      </CCarousel>
    </>
  )
}

export default Dashboard
