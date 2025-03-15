import React, { useEffect } from 'react';
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
  const alerts = useSelector((state) => state.alerts);
  const dispatch = useDispatch();

  useEffect(() => {
    const timers = alerts.map((alert, index) =>
      setTimeout(() => {
        dispatch({ type: 'removeAlert', index });
      }, 5000)
    );

    return () => timers.forEach((timer) => clearTimeout(timer));
  }, [alerts, dispatch]);

  if (alerts.length === 0) return null;

  return (
    <>
      {alerts.map((alert, index) => (
    <CAlert
      key={index}
      color={alert.type}
      className="d-flex align-items-center"
      dismissible
      onClose={() => dispatch({ type: 'removeAlert', index })}
    >
      <CIcon
        icon={iconMap[alert.type] || cilInfo}
        className="flex-shrink-0 me-2"
        width={24}
        height={24}
      />
      <div>{alert.message}</div>
    </CAlert>
      ))}
    </>
  );
};

export default AlertNotification;