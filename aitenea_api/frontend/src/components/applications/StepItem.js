/* eslint-disable consistent-return */
import React, { useState } from 'react';
import {
  Card,
  Button,
  Collapse,
  FormGroup,
  Label,
  Form,
  Input,
  Badge,
  CustomInput,
} from 'reactstrap';
import IntlMessages from '../../helpers/IntlMessages';

const StepItem = ({
  expanded,
  item,
}) => {
  const [collapse, setCollapse] = useState(expanded || false);
  const [collapseStepOptions, setCollapseStepOptions] = useState(false);
  const [collapseStepGeneticParameters, setCollapseStepGeneticParameters] = useState(false);

  return (
    <Card className={`question d-flex mb-4`}>
      <div className="d-flex flex-grow-1 min-width-zero">
        <div className="card-body align-self-center d-flex flex-column flex-md-row justify-content-between min-width-zero align-items-md-center">
          <div className="list-item-heading mb-0 truncate w-80 mb-1 mt-1">
            <span className="heading-number d-inline-block">{item.step_number}</span>
            {item.step_name}
          </div>
        </div>
        <div className="custom-control custom-checkbox pl-1 align-self-center pr-4">
          <Button
            outline
            color="theme-3"
            className={`icon-button ml-1 rotate-icon-click ${collapse ? 'rotate' : ''
              }`}
            onClick={() => setCollapse(!collapse)}
          >
            <i className="simple-icon-arrow-down" />
          </Button>
        </div>
      </div>

      <Collapse isOpen={collapse}>
        <div className="card-body pt-0">
          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.step-type" />
          </p>
          <p className="mb-3">{item.step_type}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.step-module-name" />
          </p>
          <p className="mb-3">{item.module_name}</p>

          <Button
            color="link"
            onClick={() => setCollapseStepOptions(!collapseStepOptions)}
            className="p-0"
          >
            <IntlMessages id="pline.display-step-options" />
          </Button>
          <Collapse isOpen={collapseStepOptions}>
            <p className="mb-3">
              <span className="pre">
                {JSON.stringify(item.step_options, null, '  ')}
              </span>
            </p>
          </Collapse>

          <p></p>

          <Button
            color="link"
            onClick={() => setCollapseStepGeneticParameters(!collapseStepGeneticParameters)}
            className="p-0"
          >
            <IntlMessages id="pline.display-step-genetic-parameters" />
          </Button>
          <Collapse isOpen={collapseStepGeneticParameters}>
            <p className="mb-3">
              <span className="pre">
                {JSON.stringify(item.step_genetic_parameters, null, '  ')}
              </span>
            </p>
          </Collapse>
        </div>
      </Collapse>
    </Card>
  );
}
export default StepItem;