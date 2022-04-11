/* eslint-disable react/no-danger */
import React, { useState } from 'react';
import {
  Card,
  CardBody,
  Badge,
  Collapse,
  Button
} from 'reactstrap';
import { Colxx } from '../common/CustomBootstrap';
import IntlMessages from '../../helpers/IntlMessages';

const AlgorithmDetailsCard = ({ item }) => {
  const [collapseOptions, setCollapseOptions] = useState(false);
  const [collapseGeneticParameters, setCollapseGeneticParameters] = useState(false);

  return (
    <>
      <Colxx xxs="12" lg="4" className="mb-4">
        <Card className="mb-4">
          <CardBody>
            <p className="list-item-heading mb-4">
              <IntlMessages id="menu.summary" />
            </p>
            <p className="text-muted text-small mb-2">
              <IntlMessages id="algorithm.name" />
            </p>
            <p className="mb-3">{item.class_name}</p>

            <p className="text-muted text-small mb-2">
              <IntlMessages id="algorithm.type" />
            </p>
            <p className="mb-3">{item.type}</p>

            <p className="text-muted text-small mb-2">
              <IntlMessages id="algorithm.module-name" />
            </p>
            <p className="mb-3">{item.module_name}</p>
          </CardBody>
        </Card>
      </Colxx>

      <Colxx xxs="12" lg="4" className="mb-4">
        <Card className="mb-4">
          <CardBody>
            <p className="list-item-heading mb-4">
              <IntlMessages id="menu.options" />
            </p>

            <Button
              color="link"
              onClick={() => setCollapseOptions(!collapseOptions)}
              className="p-0"
            >
              <IntlMessages id="algorithm.display-options" />
            </Button>
            <Collapse isOpen={collapseOptions}>
              <p className="mb-3">
                <span className="pre">
                  {JSON.stringify(item.options, null, '  ')}
                </span>
              </p>
            </Collapse>
          </CardBody>
        </Card>
      </Colxx>

      <Colxx xxs="12" lg="4" className="mb-4">
        <Card className="mb-4">
          <CardBody>
            <p className="list-item-heading mb-4">
              <IntlMessages id="menu.genetic-parameters" />
            </p>

            <Button
              color="link"
              onClick={() => setCollapseGeneticParameters(!collapseGeneticParameters)}
              className="p-0"
            >
              <IntlMessages id="algorithm.display-genetic-parameters" />
            </Button>
            <Collapse isOpen={collapseGeneticParameters}>
              <p className="mb-3">
                <span className="pre">
                  {JSON.stringify(item.genetic_parameters, null, '  ')}
                </span>
              </p>
            </Collapse>
          </CardBody>
        </Card>
      </Colxx>
    </>
  );
};

export default React.memo(AlgorithmDetailsCard);