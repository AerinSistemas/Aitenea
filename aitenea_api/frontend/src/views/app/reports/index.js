import React, { Suspense } from 'react';
import { Redirect, Route, Switch } from 'react-router-dom';

const ReportList = React.lazy(() =>
  import(/* webpackChunkName: "report-list" */ './list')
);
const ReportDetails = React.lazy(() =>
  import(/* webpackChunkName: "report-details" */ './details')
);

const Report = ({ match }) => (
  <Suspense fallback={<div className="loading" />}>
    <Switch>
      <Redirect exact from={`${match.url}/`} to={`${match.url}/list`} />
      <Route
        path={`${match.url}/list`}
        render={(props) => <ReportList {...props} />}
        isExact
      />
      <Route
        path={`${match.url}/details/:reportid`}
        render={(props) => <ReportDetails {...props} />}
        isExact
      />
      <Redirect to="/error" />
    </Switch>
  </Suspense>
);
export default Report;
