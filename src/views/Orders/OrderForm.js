import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CButton,
  CForm,
  CFormInput,
  CFormLabel,
  CFormSelect,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CImage,
} from '@coreui/react'
import apiService from '../../services/ApiService.js'

const OrderForm = () => {
  const { id } = useParams() // Get order ID (if editing)
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const isEditMode = Boolean(id) // True if editing, False if creating

  const [formData, setFormData] = useState({
    customer: '',
    customerEmail: '',
    trackingNumber: '',
    status: 1,
    items: [],
  })

  const [allItems, setAllItems] = useState([])
  const [selectedItem, setSelectedItem] = useState({ itemId: '', quantity: 1 })
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    if (isEditMode) {
      apiService
        .get(`orders/${id}`)
        .then((res) => {
          const data = res.data
          setFormData({
            customer: data.customer,
            customerEmail: data.customerEmail,
            trackingNumber: data.trackingNumber,
            status: data.status,
            items: data.orderItems.map((item) => ({
              itemId: item.itemId,
              quantity: item.quantity,
            })),
          })
        })
        .catch((error) => {
          console.error('Error fetching order:', error)
        })
    }

    apiService
      .get('items')
      .then((res) => {
        setAllItems(res.data)
      })
      .catch((error) => {
        console.error('Error fetching items:', error)
      })
  }, [id, isEditMode])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleItemChange = (e) => {
    const { name, value } = e.target

    // Parse quantity as an integer
    if (name === 'quantity') {
      setSelectedItem((prev) => ({
        ...prev,
        [name]: parseInt(value, 10) || 1,
      }))
    } else {
      setSelectedItem((prev) => ({
        ...prev,
        [name]: parseInt(value, 10),
      }))
    }
  }

  const handleQuantityChange = (e, index) => {
    const updatedItems = [...formData.items]
    updatedItems[index].quantity = parseInt(e.target.value, 10) || 1
    setFormData((prev) => ({
      ...prev,
      items: updatedItems,
    }))
  }

  const handleAddItem = () => {
    if (!selectedItem.itemId || selectedItem.itemId === '') {
      return
    }

    setFormData((prev) => ({
      ...prev,
      items: [...prev.items, selectedItem],
    }))
    setSelectedItem({ itemId: '', quantity: 1 })
  }

  const handleRemoveItem = (index) => {
    setFormData((prev) => ({
      ...prev,
      items: prev.items.filter((_, i) => i !== index),
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const method = isEditMode ? 'PATCH' : 'POST'
    const endpoint = isEditMode ? `orders/${id}/update` : `orders/create`

    try {
      const response = await apiService({
        method,
        url: endpoint,
        data: formData,
      })

      if (response.status === 200 || 201) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: `Save order: ${formData.customer} successfully!` },
        })
        navigate('/orders') // Redirect to order list
      }
    } catch (error) {
      console.error('Error saving order:', error)
    }
  }

  const handleDelete = async () => {
    try {
      const response = await apiService.delete(`orders/${id}/delete`)

      if (response.status === 200) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: `Delete orderID: ${id} successfully!` },
        })
        navigate('/orders')
      }
    } catch (error) {
      console.error('Error deleting order:', error)
    }
  }

  return (
    <>
      <CCard>
        <CCardHeader>
          <h2>{isEditMode ? `Edit Order ${id}` : 'Create Order'}</h2>
        </CCardHeader>
        <CCardBody>
          <CForm onSubmit={handleSubmit}>
            <div className="mb-3">
              <CFormLabel>
                Customer Name <span style={{ color: 'red' }}>*</span>
              </CFormLabel>
              <CFormInput
                required
                name="customer"
                value={formData.customer}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3">
              <CFormLabel>
                Customer Email <span style={{ color: 'red' }}>*</span>
              </CFormLabel>
              <CFormInput
                required
                name="customerEmail"
                type="email"
                value={formData.customerEmail}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3">
              <CFormLabel>Tracking Number</CFormLabel>
              <CFormInput
                name="trackingNumber"
                value={formData.trackingNumber}
                onChange={handleChange}
              />
            </div>
            {isEditMode && (
              <div className="mb-3">
                <CFormLabel>
                  Status <span style={{ color: 'red' }}>*</span>
                </CFormLabel>
                <CFormSelect name="status" value={formData.status} onChange={handleChange}>
                  <option value={1}>Received</option>
                  <option value={2}>Paid</option>
                  <option value={4}>Packed</option>
                  <option value={5}>In transit</option>
                  <option value={6}>Complete</option>
                </CFormSelect>
              </div>
            )}
            <div className="mb-3">
              <CFormLabel>Add Item</CFormLabel>
              <div className="d-flex">
                <CFormSelect
                  name="itemId"
                  value={selectedItem.itemId}
                  onChange={handleItemChange}
                  className="me-2"
                >
                  <option value="">Select Item</option>
                  {allItems
                    .filter(
                      (item) => !formData.items.some((orderItem) => orderItem.itemId === item.id),
                    ) // Filter out already selected items
                    .map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.name}
                      </option>
                    ))}
                </CFormSelect>
                <CFormInput
                  type="number"
                  name="quantity"
                  value={selectedItem.quantity}
                  onChange={handleItemChange}
                  className="me-2"
                />
                <CButton color="primary" onClick={handleAddItem}>
                  Add
                </CButton>
              </div>
            </div>
            <CTable>
              <CTableHead>
                <CTableRow>
                  <CTableHeaderCell>Item image</CTableHeaderCell>
                  <CTableHeaderCell>Item Name</CTableHeaderCell>
                  <CTableHeaderCell>Price</CTableHeaderCell>
                  <CTableHeaderCell>Quantity</CTableHeaderCell>
                  <CTableHeaderCell></CTableHeaderCell>
                </CTableRow>
              </CTableHead>
              <CTableBody>
                {formData.items.map((item, index) => {
                  const itemDetails = allItems.find((i) => i.id === item.itemId)
                  return (
                    <CTableRow key={index}>
                      <CTableDataCell>
                        {itemDetails.image ? (
                          <CImage
                            src={itemDetails?.image}
                            alt={itemDetails?.name}
                            width={80}
                            height={80}
                            style={{ objectFit: 'cover', borderRadius: '5px' }}
                          />
                        ) : (
                          <CImage
                            src="../images/404.png"
                            alt={itemDetails?.image}
                            width={80}
                            height={80}
                            style={{ objectFit: 'cover', borderRadius: '5px' }}
                          />
                        )}
                      </CTableDataCell>
                      <CTableDataCell>{itemDetails?.name}</CTableDataCell>
                      <CTableDataCell>{itemDetails?.price.toLocaleString()} baht</CTableDataCell>
                      <CTableDataCell>
                        <CFormInput
                          type="number"
                          value={item.quantity}
                          onChange={(e) => handleQuantityChange(e, index)}
                          min={1}
                        />
                      </CTableDataCell>
                      <CTableDataCell>
                        <CButton color="danger" size="sm" onClick={() => handleRemoveItem(index)}>
                          Remove
                        </CButton>
                      </CTableDataCell>
                    </CTableRow>
                  )
                })}
              </CTableBody>
            </CTable>
            <div className="d-flex justify-content-between mt-3">
              <CButton color="secondary" className="me-2" onClick={() => navigate('/orders')}>
                Back
              </CButton>
              <div>
                {isEditMode && (
                  <CButton color="danger" className="me-2" onClick={() => setShowModal(true)}>
                    Delete Order
                  </CButton>
                )}
                <CButton type="submit" color="primary">
                  {isEditMode ? 'Update Order' : 'Create Order'}
                </CButton>
              </div>
            </div>
          </CForm>
        </CCardBody>

        {/* Delete Warning Modal */}
        <CModal visible={showModal} onClose={() => setShowModal(false)}>
          <CModalHeader>⚠️ Warning</CModalHeader>
          <CModalBody>Are you sure you want to delete this order?</CModalBody>
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

export default OrderForm
