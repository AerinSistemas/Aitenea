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

const PlineDetailsCard = ({ item, status }) => {
  const [collapse, setCollapse] = useState(false);

  return (
    <Colxx xxs="12" lg="4" className="mb-4">
      <Card className="mb-4">
        <CardBody>
          <p className="list-item-heading mb-4">
            <IntlMessages id="menu.summary" />
          </p>
          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.name" />
          </p>
          <p className="mb-3">{item.name}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.description" />
          </p>
          <p className="mb-3">{item.description}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.creation-date" />
          </p>
          <p className="mb-3">{new Date(item.creation_timestamp).toLocaleString()}</p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.status" />
          </p>
          <div>
            <p className="d-sm-inline-block mb-1">
              {status !== undefined ?
                (status.error === true ?
                  <Badge color={"danger"} pill>
                    <IntlMessages id="pline.error" />
                  </Badge>
                  :
                  (status.completed === true ?
                    <Badge color={"success"} pill>
                      <IntlMessages id="pline.completed" />
                    </Badge>
                    :
                    <Badge color={"warning"} pill>
                      <IntlMessages id="pline.running" />
                    </Badge>
                  )
                )
                :
                <Badge color={"danger"} pill>
                  <IntlMessages id="pline.error" />
                </Badge>
              }
            </p>
            <p className="d-sm-inline-block  mb-1" />
          </div>

          <p></p>

          <p className="text-muted text-small mb-2">
            <IntlMessages id="pline.fitted" />
          </p>
          <div>
            <p className="d-sm-inline-block mb-1">
              {item.fitted ?
                <Badge color={"outline-success"} pill>
                  <IntlMessages id="pline.fitted" />
                </Badge>
                :
                <Badge color={"outline-danger"} pill>
                  <IntlMessages id="pline.not-fitted" />
                </Badge>
              }
            </p>
            <p className="d-sm-inline-block  mb-1" />
          </div>

          <p></p>

          <Button
            color="link"
            onClick={() => setCollapse(!collapse)}
            className="p-0"
          >
            <IntlMessages id="pline.display-metadata" />
          </Button>
          <Collapse isOpen={collapse}>
            <p className="mb-3">
              <span className="pre">
                {JSON.stringify(item.metadata, null, '  ')}
              </span>
            </p>
          </Collapse>

        </CardBody>
      </Card>
    </Colxx>
  );
};

export default React.memo(PlineDetailsCard);