import React, { Suspense } from 'react';
import { Route, withRouter, Switch, Redirect } from 'react-router-dom';
import { connect } from 'react-redux';

import AppLayout from '../../layout/AppLayout';
// import { ProtectedRoute, UserRole } from '../../helpers/authHelper';

const Pline = React.lazy(() =>
  import(/* webpackChunkName: "views-pline" */ './pline')
);
const Report = React.lazy(() =>
  import(/* webpackChunkName: "views-reports" */ './reports')
);
const Algorithm = React.lazy(() =>
  import(/* webpackChunkName: "views-algorithm" */ './algorithm')
);

const App = ({ match }) => {
  return (
    <AppLayout>
      <div className="dashboard-wrapper">
        <Suspense fallback={<div className="loading" />}>
          <Switch>
            <Redirect exact from={`${match.url}/`} to={`${match.url}/pline`} />
            <Route
              path={`${match.url}/pline`}
              render={(props) => <Pline {...props} />}
            />
            <Route
              path={`${match.url}/report`}
              render={(props) => <Report {...props} />}
            />
            <Route
              path={`${match.url}/algorithm`}
              render={(props) => <Algorithm {...props} />}
            />
            {/* 
            <ProtectedRoute
                    path={`${match.url}/reports`}
                    component={Reports}
                    roles={[UserRole.Admin]}
            /> 
            */}
            <Redirect to="/error" />
          </Switch>
        </Suspense>
      </div>
    </AppLayout>
  );
};

const mapStateToProps = ({ menu }) => {
  const { containerClassnames } = menu;
  return { containerClassnames };
};

export default withRouter(connect(mapStateToProps, {})(App));
