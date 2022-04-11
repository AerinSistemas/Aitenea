/* eslint-disable react/no-danger */
import React, { useState } from 'react';
import {
  Card,
  CardBody,
  Badge,
  Collapse,
  Button,
  Nav,
  NavItem,
  NavLink
} from 'reactstrap';
import { Colxx } from '../common/CustomBootstrap';
import IntlMessages from '../../helpers/IntlMessages';

import { adminRoot } from '../../constants/defaultValues';

const PlineReportDetailsCard = ({ item }) => {
  const [collapseSteps, setCollapseSteps] = useState(false);
  const [collapseDatasetParameters, setCollapseDatasetParameters] = useState(false);
  const [collapseErrorOutput, setCollapseErrorOutput] = useState(false);

  return (
    <Colxx xxs="12" lg="6" className="mb-4">
      <Card className="mb-4">
        <CardBody>
          <p className="list-item-heading mb-4">
            <IntlMessages id="menu.summary" />
          </p>
          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.name" />
          </p>
          <p className="mb-3">{item.pline_name}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="reports.creation-date" />
          </p>
          <p className="mb-3">{new Date(item.created_at).toLocaleString()}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="reports.execution-time" />
          </p>
          <p className="mb-3">{item.execution_time}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="reports.train-dataset-percentage" />
          </p>
          <p className="mb-3">{item.train_dataset_percentage}%</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="reports.test-dataset-percentage" />
          </p>
          <p className="mb-3">{item.test_dataset_percentage}%</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="reports.origin-dataset" />
          </p>
          <p className="mb-3">{item.origin_dataset}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="reports.target-dataset" />
          </p>
          <p className="mb-3">{item.target_dataset}</p>

          <p></p>

          <Button
            color="link"
            onClick={() => setCollapseSteps(!collapseSteps)}
            className="p-0"
          >
            <IntlMessages id="reports.display-steps" />
          </Button>
          <Collapse isOpen={collapseSteps}>
            <p className="mb-3">
              <span className="pre">
                {JSON.stringify(item.steps, null, '  ')}
              </span>
            </p>
          </Collapse>

          <p></p>

          <Button
            color="link"
            onClick={() => setCollapseDatasetParameters(!collapseDatasetParameters)}
            className="p-0"
          >
            <IntlMessages id="reports.display-dataset-parameters" />
          </Button>
          <Collapse isOpen={collapseDatasetParameters}>
            <p className="mb-3">
              <span className="pre">
                {JSON.stringify(item.dataset_parameters, null, '  ')}
              </span>
            </p>
          </Collapse>

          <p></p>

          {item.error_output != null ?
            <>
              <Button
                color="link"
                onClick={() => setCollapseErrorOutput(!collapseErrorOutput)}
                className="p-0"
              >
                <IntlMessages id="reports.display-error-output" />
              </Button>
              <Collapse isOpen={collapseErrorOutput}>
                <p className="mb-3">
                  <span className="pre">
                    {JSON.stringify(item.error_output, null, '  ')}
                  </span>
                </p>
              </Collapse>
            </>
            :
            <>
              <p className="text-muted text-small mb-2">
                <IntlMessages id="reports.error-output" />
              </p>
              <p className="mb-3">
                <IntlMessages id="reports.no-error-logs" />
              </p>
            </>
          }

          {item.pline != null ?
            <Nav pills className="nav-fill">
              <NavItem>
                <NavLink
                  active
                  href={`${adminRoot}/pline/details/${item.pline}`}
                >
                  <IntlMessages id="reports.display-related-pline" />
                </NavLink>
              </NavItem>
            </Nav>
            :
            ''
          }

        </CardBody>
      </Card>
    </Colxx>
  );
};

export default React.memo(PlineReportDetailsCard);