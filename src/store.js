import { legacy_createStore as createStore } from 'redux'

const initialState = {
  sidebarShow: true,
  theme: 'light',
  alert: null,
}

const changeState = (state = initialState, action) => {
  switch (action.type) {
    case 'set':
      return { ...state, ...action.payload };
    case 'setAlert':
      return { ...state, alert: action.alert };
    default:
      return state;
  }
};

const store = createStore(changeState)
export default store
