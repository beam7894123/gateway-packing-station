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
} from '@coreui/react'
import { useNavigate } from 'react-router-dom'
import apiService from '../../services/ApiService.js'
import { useDispatch } from 'react-redux'

const Items = () => {
  const navigate = useNavigate()
  const dispatch = useDispatch()

  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true) // Add loading state
  const [showModal, setShowModal] = useState(false)
  const [selectedItemId, setSelectedItemId] = useState(null) // Add state for selected item ID

  useEffect(() => {
    apiService
      .get('items')
      .then((response) => {
        setItems(response.data)
        setLoading(false) // Set loading to false after data is fetched
      })
      .catch((error) => {
        console.error('Error fetching items:', error)
        setLoading(false) // Set loading to false in case of error
      })
  }, [])

  const handleDelete = async () => {
    try {
      const response = await apiService.delete(`items/${selectedItemId}/delete`)
      if (response.status === 200) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: 'Delete item successfully!' },
        })
        navigate('/items')
        window.location.reload()
      }
    } catch (error) {
      console.error('Error deleting item:', error)
    }
  }

  return (
    <>
      <CCardHeader className="mb-4">
        <h1>Items List</h1>
      </CCardHeader>
      <CCard className="mb-2">
        <CCardBody>
          <div className="d-grid gap-2">
            {loading === false ? (
              <CButton onClick={() => navigate(`/item/new`)} color="primary">
                + Add Item
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
          {loading ? (
            <div className="text-center">
              <CSpinner color="primary" />
            </div>
          ) : items.length > 0 ? (
            <CTable striped>
              <CTableHead>
                <CTableRow>
                  <CTableHeaderCell>Image</CTableHeaderCell>
                  <CTableHeaderCell>Name</CTableHeaderCell>
                  <CTableHeaderCell>Price</CTableHeaderCell>
                  <CTableHeaderCell>Quantity</CTableHeaderCell>
                  <CTableHeaderCell></CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {items.map((item, index) => (
                  <CTableRow key={item.id}>
                    <CTableDataCell>
                      {item.image ? (
                        <CImage
                          src={item.image}
                          alt={item.name}
                          width={100}
                          height={100}
                          style={{ objectFit: 'cover', borderRadius: '5px' }}
                        />
                      ) : (
                        <CImage
                          src="../images/404.png"
                          alt={item.name}
                          width={100}
                          height={100}
                          style={{ objectFit: 'cover', borderRadius: '5px' }}
                        />
                      )}
                    </CTableDataCell>
                    <CTableDataCell>{item.name}</CTableDataCell>
                    <CTableDataCell>{item.price.toLocaleString()} baht</CTableDataCell>
                    <CTableDataCell>{item.quantity}</CTableDataCell>
                    <CTableDataCell>
                      <CDropdown variant="btn-group">
                        <CButton color="primary" onClick={() => navigate(`/item/${item.id}`)}>
                          Edit
                        </CButton>
                        <CDropdownToggle color="primary" />
                        <CDropdownMenu>
                          <CDropdownItem
                            onClick={() => {
                              setSelectedItemId(item.id)
                              setShowModal(true)
                            }}
                          >
                            Delete
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

export default Items
