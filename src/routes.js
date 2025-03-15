import React from 'react'

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'))
const Orders = React.lazy(() => import('./views/Orders/Orders'))
const OrderForm = React.lazy(() => import('./views/Orders/OrderForm'))
const Items = React.lazy(() => import('./views/Items/Items'))
const ItemForm = React.lazy(() => import('./views/Items/ItemForm'))

const routes = [
  { path: '/', exact: true, name: 'Home' },
  { path: '/dashboard', name: 'Dashboard', element: Dashboard },
  { path: '/orders', name: 'Orders', element: Orders },
  { path: '/order/new', name: 'New Order', element: OrderForm },
  { path: '/order/:id', name: 'Edit Order', element: OrderForm },
  { path: '/items', name: 'Items', element: Items },
  { path: '/item/new', name: 'New Item', element: ItemForm },
  { path: '/item/:id', name: 'Edit Item', element: ItemForm },

  
]

export default routes
