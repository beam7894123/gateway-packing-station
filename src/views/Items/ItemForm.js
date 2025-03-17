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
  CFormTextarea,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CInputGroupText,
  CInputGroup,
} from '@coreui/react'
import apiService from '../../services/ApiService.js'

const ItemForm = () => {
  const { id } = useParams() // Get item ID (if editing)
  const navigate = useNavigate()
  const dispatch = useDispatch()
  const isEditMode = Boolean(id) // True if editing, False if creating
  const apiUrl = import.meta.env.VITE_BASE_API_URL

  const [formData, setFormData] = useState({
    itemCode: '',
    name: '',
    description: '',
    price: '',
    quantity: '',
    image: null,
    imagePreview: '',
  })

  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    if (isEditMode) {
      apiService
        .get(`items/${id}`)
        .then((res) => {
          const data = res.data
          setFormData({
            itemCode: data.itemCode,
            name: data.name,
            description: data.description,
            price: data.price,
            quantity: data.quantity,
            image: null,
            imagePreview: data.image,
          })
        })
        .catch((error) => {
          console.error('Error fetching item:', error)
        })
    }
  }, [id, isEditMode])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setFormData((prev) => ({
        ...prev,
        image: file,
        imagePreview: URL.createObjectURL(file),
      }))
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const form = new FormData()
    form.append('itemCode', formData.itemCode)
    form.append('name', formData.name)
    form.append('description', formData.description)
    form.append('price', formData.price)
    form.append('quantity', formData.quantity)
    if (formData.image) {
      form.append('image', formData.image)
    }

    const method = isEditMode ? 'PATCH' : 'POST'
    const endpoint = isEditMode ? `items/${id}/update` : `items/create`

    try {
      const response = await apiService({
        method,
        url: endpoint,
        data: form,
      })

      if (response.status === 200 || response.status === 201) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: `Save item: ${formData.name} successfully!` },
        })
        navigate('/items') // Redirect to item list
      }
    } catch (error) {
      console.error('Error saving item:', error)
    }
  }

  const handleDelete = async () => {
    try {
      const response = await apiService.delete(`items/${id}/delete`)

      if (response.status === 200) {
        dispatch({
          type: 'addAlert',
          alert: { type: 'success', message: `Delete item: ${formData.name} successfully!` },
        })
        navigate('/items')
      }
    } catch (error) {
      console.error('Error deleting item:', error)
    }
  }

  return (
    <>
      <CCard>
        <CCardHeader>
          <h2>{isEditMode ? 'Edit Item' : 'Create Item'}</h2>
        </CCardHeader>
        <CCardBody>
          <CForm onSubmit={handleSubmit}>
            <div className="mb-3 text-center">
              {formData.imagePreview && (
                <img src={formData.imagePreview} alt="Preview" className="mt-2 mb-4" height={300} />
              )}
              <CFormInput type="file" accept="image/*" onChange={handleFileChange} />
            </div>
            <div className="mb-3">
              <CFormLabel>Item Code</CFormLabel>
              <CFormInput
                name="itemCode"
                value={formData.itemCode}
                placeholder="Leave it blank for auto generate"
                onChange={handleChange}
              />
            </div>
            <div className="mb-3">
              <CFormLabel>
                Name <span style={{ color: 'red' }}>*</span>
              </CFormLabel>
              <CFormInput name="name" required value={formData.name} onChange={handleChange} />
            </div>
            <div className="mb-3">
              <CFormLabel>Description</CFormLabel>
              <CFormTextarea
                name="description"
                value={formData.description}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3">
              <CFormLabel>
                Price <span style={{ color: 'red' }}>*</span>
              </CFormLabel>
              <CInputGroup>
                <CFormInput
                  required
                  type="number"
                  name="price"
                  value={formData.price}
                  onChange={handleChange}
                />
                <CInputGroupText>Baht</CInputGroupText>
              </CInputGroup>
            </div>
            <div className="mb-3">
              <CFormLabel>
                Quantity <span style={{ color: 'red' }}>*</span>
              </CFormLabel>
              <CFormInput
                required
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
              />
            </div>
            <div className="d-flex justify-content-between">
              <CButton color="secondary" className="me-2" onClick={() => navigate('/items')}>
                Back
              </CButton>
              <div>
                {isEditMode && (
                  <CButton color="danger" className="me-2" onClick={() => setShowModal(true)}>
                    Delete Item
                  </CButton>
                )}
                <CButton type="submit" color="primary">
                  {isEditMode ? 'Update Item' : 'Create Item'}
                </CButton>
              </div>
            </div>
          </CForm>
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

export default ItemForm
