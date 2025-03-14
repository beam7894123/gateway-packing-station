// src/components/AlertNotification.js
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { CAlert } from '@coreui/react';
import CIcon from '@coreui/icons-react';
import { cilCheckCircle, cilWarning, cilInfo } from '@coreui/icons';

const iconMap = {
  success: cilCheckCircle,
  danger: cilWarning,
  warning: cilWarning,
  primary: cilInfo,
};

const AlertNotification = () => {
  const alert = useSelector((state) => state.alert);
  const dispatch = useDispatch();

  if (!alert) return null;

  return (
    <CAlert
      color={alert.type}
      className="d-flex align-items-center"
      dismissible
      onClose={() => dispatch({ type: 'setAlert', alert: null })}
    >
      <CIcon
        icon={iconMap[alert.type] || cilInfo}
        className="flex-shrink-0 me-2"
        width={24}
        height={24}
      />
      <div>{alert.message}</div>
    </CAlert>
  );
};

export default AlertNotification;