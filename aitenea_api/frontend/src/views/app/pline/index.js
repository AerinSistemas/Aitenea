import React, { Suspense } from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

const PlineList = React.lazy(() =>
  import(/* webpackChunkName: "pline-list" */ './list')
);
const PlineDetails = React.lazy(() =>
  import(/* webpackChunkName: "pline-details" */ './details')
);

const Pline = ({ match }) => (
  <Suspense fallback={<div className="loading" />}>
    <Switch>
      <Redirect exact from={`${match.url}/`} to={`${match.url}/list`} />
      <Route
        path={`${match.url}/list`}
        render={(props) => <PlineList {...props} />}
        isExact
      />
      <Route
        path={`${match.url}/details/:plineid`}
        render={(props) => <PlineDetails {...props} />}
        isExact
      />
      <Redirect to="/error" />
    </Switch>
  </Suspense>
);
export default Pline;
