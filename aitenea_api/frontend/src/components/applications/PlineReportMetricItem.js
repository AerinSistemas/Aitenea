/* eslint-disable consistent-return */
import React, { useState } from 'react';
import {
  Card,
} from 'reactstrap';
import IntlMessages from '../../helpers/IntlMessages';

const PlineReportMetricItem = ({
  item,
}) => {

  return (
    <Card className={`question d-flex mb-4`}>
      <div className="d-flex flex-grow-1 min-width-zero">
        <div className="card-body align-self-center d-flex flex-column flex-md-row justify-content-between min-width-zero align-items-md-center">
          <div className="list-item-heading mb-0 truncate w-80 mb-1 mt-1">
            {item.metric_name}
          </div>
        </div>
      </div>
      <div className="card-body pt-0">
        <p className="text-muted text-small mb-2">
          {item.score.toString()}
        </p>
      </div>
    </Card>
  );
}
export default PlineReportMetricItem;