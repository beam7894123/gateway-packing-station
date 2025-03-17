import React from 'react'
import {
  CButton,
  CCol,
  CContainer,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
  CImage
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilMagnifyingGlass } from '@coreui/icons'

const Page404 = () => {
  return (
    <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center text-center">                  
          <CCol md={6}>
          <CImage 
              src="../images/404.png"
              height={300} 
              className='text-center'
              style={{ objectFit: "cover", borderRadius: "5px" }} 
            />
            <div className="clearfix">
              <h4 className="pt-3">Oops! Look like you{"'"}re lost.</h4>
              <p className="text-body-secondary">
                The page you are looking for was not found =m=
              </p>
            </div>
            {/* <CInputGroup className="input-prepend">
              <CInputGroupText>
                <CIcon icon={cilMagnifyingGlass} />
              </CInputGroupText>
              <CFormInput type="text" placeholder="What are you looking for?" />
              <CButton color="info">Search</CButton>
            </CInputGroup> */}
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Page404
