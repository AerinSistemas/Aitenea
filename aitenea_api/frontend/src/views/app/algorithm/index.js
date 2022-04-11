import React, { Suspense } from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

const AlgorithmList = React.lazy(() =>
  import(/* webpackChunkName: "algorithm-list" */ './list')
);
const AlgorithmDetails = React.lazy(() =>
  import(/* webpackChunkName: "algorithm-details" */ './details')
);

const Algorithm = ({ match }) => (
  <Suspense fallback={<div className="loading" />}>
    <Switch>
      <Redirect exact from={`${match.url}/`} to={`${match.url}/list`} />
      <Route
        path={`${match.url}/list`}
        render={(props) => <AlgorithmList {...props} />}
        isExact
      />
      <Route
        path={`${match.url}/details/:algorithmid`}
        render={(props) => <AlgorithmDetails {...props} />}
        isExact
      />
      <Redirect to="/error" />
    </Switch>
  </Suspense>
);
export default Algorithm;
