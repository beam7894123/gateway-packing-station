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
  CDropdown,
  CDropdownToggle,
  CDropdownMenu,
  CDropdownItem,
  CImage,
  CButton,
  CPlaceholder,
  CSpinner,
  CCardHeader,
  CModal,
  CModalHeader,
  CModalBody,
  CModalFooter,
  CBadge,
  CDropdownDivider,
  CFormSelect,
  CFormInput,
  CFormLabel,
  CRow,
  CCol,
} from '@coreui/react'
import { useNavigate } from 'react-router-dom'
import apiService from '../../services/ApiService.js'
import { useDispatch } from 'react-redux'

const Orders = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()

  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [selectedItemId, setSelectedItemId] = useState(null)
  const [buttonLoading, setButtonLoading] = useState(false)
  const [sortOrder, setSortOrder] = useState('asc') // State to manage sorting order
  const [statusFilter, setStatusFilter] = useState('') // State to manage status filter
  const [dateFilter, setDateFilter] = useState('') // State to manage date filter

  const statusColors = {
    1: 'secondary', // received
    2: 'primary', // paid
    3: 'warning', // packing
    4: 'info', // Packed
    5: 'info', // in transit
    6: 'success', // complete
  }

  const statusLabels = {
    1: 'Payment is Pending',
    2: 'Paid (Ready for Packing)',
    3: 'Packing',
    4: 'Packed',
    5: 'In Transit',
    6: 'Complete',
  }

  useEffect(() => {
    apiService
      .get('orders')
      .then((response) => {
        setItems(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.error('Error fetching items:', error)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    handleFilter()
  }, [statusFilter, dateFilter])

  const handlePrintPickingList = async (itemId) => {
    setButtonLoading(true)
    setSelectedItemId(itemId) // Ensure selectedItemId is set
    try {
      const response = await apiService.get(`orders/${itemId}/picking-list`)
      if (response.status === 200) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: 'Print picking list successfully!' },
        })
        window.open(response.data.url, '_blank') // Open the URL in a new tab
      }
    } catch (error) {
      dispatch({
        type: 'addAlert',
        alert: { type: 'danger', message: 'Error printing picking list!' },
      })
      console.error('Error printing picking list:', error)
    } finally {
      setButtonLoading(false) // Set button loading state to false
    }
  }

  const handleSetStatus = async (itemId, status) => {
    setButtonLoading(true)
    try {
      const response = await apiService.patch(`orders/${itemId}/set/status`, { status: status })
      if (response.status === 200) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: 'Order status updated successfully!' },
        })
        navigate('/orders')
        window.location.reload()
      }
    } catch (error) {
      dispatch({
        type: 'addAlert',
        alert: { type: 'danger', message: 'Error updating order status!' },
      })
      console.error('Error updating order status:', error)
    } finally {
      setButtonLoading(false)
    }
  }

  const handleDelete = async () => {
    try {
      const response = await apiService.delete(`orders/${selectedItemId}/delete`)
      if (response.status === 200) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: 'Delete order successfully!' },
        })
        navigate('/orders')
        window.location.reload()
      }
    } catch (error) {
      console.error('Error deleting item:', error)
    }
  }

  const handleSort = () => {
    const sortedItems = [...items].sort((a, b) => {
      if (sortOrder === 'asc') {
        return a.id - b.id
      } else {
        return b.id - a.id
      }
    })
    setItems(sortedItems)
    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
  }

  const handleClearFilter = () => {
    setStatusFilter('')
    setDateFilter('')
  }

  const handleFilter = () => {
    apiService
      .get('orders', {
        params: {
          status: statusFilter,
          createdAt: dateFilter,
        },
      })
      .then((response) => {
        setItems(response.data)
      })
      .catch((error) => {
        console.error('Error fetching filtered items:', error)
      })
  }

  return (
    <>
      <CCardHeader className="mb-4">
        <h1>Order List</h1>
      </CCardHeader>
      <CCard className="mb-2">
        <CCardBody>
          <div className="d-grid gap-2">
            {loading === false ? (
              <CButton onClick={() => navigate(`/order/new`)} color="primary">
                + Add Order
              </CButton>
            ) : (
              <CPlaceholder
                as={CButton}
                color="primary"
                aria-hidden="true"
                disabled
                href="#"
                xs={12}
              />
            )}
          </div>
        </CCardBody>
      </CCard>

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
                  <option value="1">Payment is Pending</option>
                  <option value="2">Paid (Ready for Packing)</option>
                  <option value="3">Packing</option>
                  <option value="4">Packed</option>
                  <option value="5">In Transit</option>
                  <option value="6">Complete</option>
                </CFormSelect>
              </CCol>
              <CCol>
                <CFormLabel className="me-2">Created Date:</CFormLabel>
                <CFormInput
                  type="date"
                  className="me-2"
                  value={dateFilter}
                  onChange={(e) => setDateFilter(e.target.value)}
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
                  <CTableHeaderCell onClick={handleSort} style={{ cursor: 'pointer' }}>
                    OrderID {sortOrder === 'asc' ? '↑' : '↓'}
                  </CTableHeaderCell>
                  <CTableHeaderCell>Customer Name</CTableHeaderCell>
                  <CTableHeaderCell>Status</CTableHeaderCell>
                  <CTableHeaderCell>Tracking Number</CTableHeaderCell>
                  <CTableHeaderCell>Created</CTableHeaderCell>
                  <CTableHeaderCell></CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {items.map((item, index) => (
                  <CTableRow key={item.id}>
                    <CTableDataCell>{item.id}</CTableDataCell>
                    <CTableDataCell>{item.customer}</CTableDataCell>
                    <CTableDataCell>
                      <CBadge color={statusColors[item.status]}>{statusLabels[item.status]}</CBadge>
                    </CTableDataCell>
                    <CTableDataCell>{item.trackingNumber || 'None'}</CTableDataCell>
                    <CTableDataCell>{new Date(item.createdAt).toLocaleString()}</CTableDataCell>
                    <CTableDataCell>
                      <CDropdown variant="btn-group">
                        <CButton
                          disabled={item.status === 3}
                          color="primary"
                          onClick={() => navigate(`/order/${item.id}`)}
                        >
                          {buttonLoading ? <CSpinner size="sm" /> : 'Edit'}
                        </CButton>
                        <CDropdownToggle disabled={item.status === 3} color="primary" />
                        <CDropdownMenu>
                          <CDropdownItem onClick={() => handlePrintPickingList(item.id)}>
                            {buttonLoading ? <CSpinner size="sm" /> : 'Print picking list'}
                          </CDropdownItem>
                          <CDropdownItem
                            onClick={() => {
                              setSelectedItemId(item.id)
                              setShowModal(true)
                            }}
                          >
                            Delete
                          </CDropdownItem>
                          <CDropdownDivider />
                          <p className="px-3 mb-0 text-body-secondary">Set order to</p>
                          <CDropdownItem
                            onClick={() => {
                              handleSetStatus(item.id, 2)
                            }}
                          >
                            Paid
                          </CDropdownItem>
                          <CDropdownItem
                            onClick={() => {
                              handleSetStatus(item.id, 5)
                              setShowModal(true)
                            }}
                          >
                            In Transit
                          </CDropdownItem>
                          <CDropdownItem
                            onClick={() => {
                              handleSetStatus(item.id, 6)
                              setShowModal(true)
                            }}
                          >
                            Complete
                          </CDropdownItem>
                        </CDropdownMenu>
                      </CDropdown>
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
        <CModal visible={showModal} onClose={() => setShowModal(false)}>
          <CModalHeader>⚠️ Warning</CModalHeader>
          <CModalBody>Are you sure you want to delete this item?</CModalBody>
          <CModalFooter>
            <CButton color="secondary" onClick={() => setShowModal(false)}>
              Cancel
            </CButton>
            <CButton color="danger" onClick={handleDelete}>
              Delete
            </CButton>
          </CModalFooter>
        </CModal>
      </CCard>
    </>
  )
}

export default Orders
