import React, { useEffect, useState } from 'react'
import {
  CCard,
  CCardBody,
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CButton,
  CPlaceholder,
  CSpinner,
  CBadge,
  CCardHeader,
  CModal,
  CModalHeader,
  CModalBody,
  CModalFooter,
  CDropdown,
  CDropdownToggle,
  CDropdownMenu,
  CDropdownItem,
  CDropdownDivider,
  CFormLabel,
  CFormSelect,
  CFormInput,
  CRow,
  CCol,
} from '@coreui/react'
import { useNavigate } from 'react-router-dom'
import apiService from '../../services/ApiService.js'
import { useDispatch } from 'react-redux'

const Packing = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()

  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [buttonLoading, setButtonLoading] = useState(false)
  const [showModalDelete, setShowModalDelete] = useState(false)
  const [showModalResendEmail, setShowModalResendEmail] = useState(false)
  const [showModalSendEmail, setShowModalSendEmail] = useState(false)
  const [selectedItemId, setSelectedItemId] = useState(null)
  const [statusFilter, setStatusFilter] = useState('')
  // const [dateFilter, setDateFilter] = useState('')
  const [startDateFilter, setStartDateFilter] = useState('')
  const [endDateFilter, setEndDateFilter] = useState('')

  const statusColors = {
    0: 'danger', // packing failed
    1: 'warning', // packing
    2: 'info', // finished
    3: 'success', // email sent
  }

  const statusLabels = {
    0: 'Packing Failed',
    1: 'Packing',
    2: 'Finished',
    3: 'Email Sent',
  }

  useEffect(() => {
    handleFilter()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter, startDateFilter, endDateFilter])

  const handleFilter = () => {
    setLoading(true)
    const params = {
      status: statusFilter || undefined,
      startDate: startDateFilter || undefined,
      endDate: endDateFilter || undefined,
    }

    apiService
      .get('packing', {
        params: params,
      })
      .then((response) => {
        setItems(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error fetching filtered packing data:', error)
        dispatch({
          type: 'addAlert',
          alert: { type: 'danger', message: 'Error fetching packing data!' },
        })
        setLoading(false)
      })
  }

  const handleClearFilter = () => {
    setStatusFilter('')
    setStartDateFilter('')
    setEndDateFilter('')
  }

  const handleViewVideo = (videoUrl) => {
    window.open(videoUrl, '_blank') // Open video in a new tab
  }

  const handleResendEmail = async () => {
    try {
      setShowModalResendEmail(false)
      setLoading(true)
      const response = await apiService.post(`packing/${selectedItemId}/mail/send`)
      if (response.status === 200 || response.status === 201) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: 'Resend email successfully!' },
        })
        setLoading(false)
      }
    } catch (error) {
      console.error('Error resending email:', error)
      setLoading(false)
    }
  }

  const handleSendEmail = async () => {
    try {
      setShowModalResendEmail(false)
      setLoading(true)
      const response = await apiService.post(`packing/${selectedItemId}/mail/send`)
      if (response.status === 200 || response.status === 201) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: 'Send email successfully!' },
        })
        setLoading(false)
        navigate('/packing')
        window.location.reload()
      }
    } catch (error) {
      console.error('Error sending email:', error)
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    try {
      const response = await apiService.delete(`packing/${selectedItemId}/delete`)
      if (response.status === 200) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: 'Delete packing proof successfully!' },
        })
        navigate('/packing')
        window.location.reload()
      }
    } catch (error) {
      console.error('Error deleting item:', error)
    }
  }

  return (
    <>
      <CCardHeader className="mb-4">
        <h1>Packing Proof List</h1>
      </CCardHeader>
      <CCard className="mb-4">
        <CCardBody>
          <div className="mb-3">
            <CRow className="align-items-center">
              <CCol>
                <CFormLabel className="me-2">Status:</CFormLabel>
                <CFormSelect
                  className="me-2"
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="">All Statuses</option>
                  <option value="0">Packing Failed</option>
                  <option value="1">Packing</option>
                  <option value="2">Finished</option>
                  <option value="3">Email Sent</option>
                </CFormSelect>
              </CCol>
              <CCol md={3}>
                <CFormLabel className="me-2">Start Date:</CFormLabel>
                <CFormInput
                  type="date"
                  value={startDateFilter}
                  onChange={(e) => setStartDateFilter(e.target.value)}
                />
              </CCol>
              <CCol md={3}>
                <CFormLabel className="me-2">End Date:</CFormLabel>
                <CFormInput
                  type="date"
                  value={endDateFilter}
                  onChange={(e) => setEndDateFilter(e.target.value)}
                />
              </CCol>
              <CCol xs="auto" className="mt-4">
                <CButton color="secondary" onClick={handleClearFilter}>
                  Clear
                </CButton>
              </CCol>
            </CRow>
          </div>
          {loading ? (
            <div className="text-center">
              <CSpinner color="primary" />
            </div>
          ) : items.length > 0 ? (
            <CTable>
              <CTableHead>
                <CTableRow>
                  <CTableHeaderCell>Packing ID</CTableHeaderCell>
                  <CTableHeaderCell>Order ID</CTableHeaderCell>
                  <CTableHeaderCell>Customer</CTableHeaderCell>
                  <CTableHeaderCell>Status</CTableHeaderCell>
                  <CTableHeaderCell>Station</CTableHeaderCell>
                  <CTableHeaderCell>Packing At</CTableHeaderCell>
                  <CTableHeaderCell>Order At</CTableHeaderCell>
                  <CTableHeaderCell></CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {items.map((item) => (
                  <CTableRow key={item.id}>
                    <CTableDataCell>{item.id}</CTableDataCell>
                    <CTableDataCell>
                      <CButton color="link" onClick={() => navigate(`/order/${item.orderId}`)}>
                        {item.orderId}
                      </CButton>
                    </CTableDataCell>
                    <CTableDataCell>{item.order.customer}</CTableDataCell>
                    <CTableDataCell>
                      <CBadge color={statusColors[item.status]}>{statusLabels[item.status]}</CBadge>
                    </CTableDataCell>
                    <CTableDataCell>{item.station}</CTableDataCell>
                    <CTableDataCell>{new Date(item.createdAt).toLocaleString()}</CTableDataCell>
                    <CTableDataCell>
                      {new Date(item.order.createdAt).toLocaleString()}
                    </CTableDataCell>
                    <CTableDataCell>
                      {item.video ? (
                        <CDropdown variant="btn-group">
                          <CButton color="primary" onClick={() => handleViewVideo(item.video)}>
                            {buttonLoading ? <CSpinner size="sm" /> : 'View'}
                          </CButton>
                          <CDropdownToggle color="primary" />
                          <CDropdownMenu>
                            {item.status === 3 && (
                              <CDropdownItem
                                onClick={() => {
                                  setSelectedItemId(item.id)
                                  setShowModalResendEmail(true)
                                }}
                              >
                                Resend Email
                              </CDropdownItem>
                            )}
                            {item.status === 2 && (
                              <CDropdownItem
                                onClick={() => {
                                  setSelectedItemId(item.id)
                                  setShowModalSendEmail(true)
                                }}
                              >
                                Send Email
                              </CDropdownItem>
                            )}
                            <CDropdownItem
                              onClick={() => {
                                setSelectedItemId(item.id)
                                setShowModalDelete(true)
                              }}
                            >
                              Delete
                            </CDropdownItem>
                          </CDropdownMenu>
                        </CDropdown>
                      ) : (
                        <CButton
                          color="danger"
                          onClick={() => {
                            setSelectedItemId(item.id)
                            setShowModalDelete(true)
                          }}
                        >
                          {buttonLoading ? <CSpinner size="sm" /> : 'Delete'}
                        </CButton>
                      )}
                    </CTableDataCell>
                  </CTableRow>
                ))}
              </CTableBody>
            </CTable>
          ) : (
            <div className="text-center">
              <p>No items available</p>
            </div>
          )}
        </CCardBody>

        {/* Delete Warning Modal */}
        <CModal visible={showModalDelete} onClose={() => setShowModalDelete(false)}>
          <CModalHeader>⚠️ Warning</CModalHeader>
          <CModalBody>Are you sure you want to delete this item?</CModalBody>
          <CModalFooter>
            <CButton color="secondary" onClick={() => setShowModalDelete(false)}>
              Cancel
            </CButton>
            <CButton color="danger" onClick={handleDelete}>
              Delete
            </CButton>
          </CModalFooter>
        </CModal>

        {/* Resend Email Modal */}
        <CModal visible={showModalResendEmail} onClose={() => setShowModalResendEmail(false)}>
          <CModalHeader>Resend Email</CModalHeader>
          <CModalBody>Are you sure you want to resend the email?</CModalBody>
          <CModalFooter>
            <CButton color="secondary" onClick={() => setShowModalResendEmail(false)}>
              Cancel
            </CButton>
            <CButton color="primary" onClick={handleResendEmail}>
              Resend
            </CButton>
          </CModalFooter>
        </CModal>

        {/* Send Email Modal */}
        <CModal visible={showModalSendEmail} onClose={() => setShowModalSendEmail(false)}>
          <CModalHeader>Resend Email</CModalHeader>
          <CModalBody>Are you sure you want to send the email?</CModalBody>
          <CModalFooter>
            <CButton color="secondary" onClick={() => setShowModalSendEmail(false)}>
              Cancel
            </CButton>
            <CButton color="primary" onClick={handleSendEmail}>
              Send
            </CButton>
          </CModalFooter>
        </CModal>
      </CCard>
    </>
  )
}

export default Packing
