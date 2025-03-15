import { legacy_createStore as createStore } from 'redux';

const initialState = {
  sidebarShow: true,
  theme: 'light',
  alerts: [],
};

const changeState = (state = initialState, action) => {
  switch (action.type) {
    case 'set':
      return { ...state, ...action.payload };
    case 'addAlert':
      return { ...state, alerts: [...state.alerts, action.alert] }; // Add alert to alerts array
    case 'removeAlert':
      return { ...state, alerts: state.alerts.filter((alert, index) => index !== action.index) };
    default:
      return state;
  }
};

const store = createStore(changeState);
export default store;