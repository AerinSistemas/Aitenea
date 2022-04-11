import React, { useEffect } from 'react';
import { Route, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import {
  loadUser
} from '../redux/actions';
import history from './history';

const ProtectedRoute = ({
  component: Component,
  user,
  token,
  loadUserAction,
  ...rest
}) => {
  useEffect(() => {
    loadUserAction(history);
  }, [loadUserAction]);

  const setComponent = (props) => {
    if (token !== null && localStorage.getItem("token") !== null) {
      return <Component {...props} />;
    }
    else {
      return (
        <Redirect
          to={{
            pathname: '/user/login',
            state: { from: props.location },
          }}
        />
      );
    }
  };

  return <Route {...rest} render={setComponent} />;
};

const mapStateToProps = state => ({
  user: state.authUser.currentUser,
  token: state.authUser.token
});

// eslint-disable-next-line import/prefer-default-export
export default connect(mapStateToProps, {
  loadUserAction: loadUser,
})(ProtectedRoute);
