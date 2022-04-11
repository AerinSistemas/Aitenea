import React from 'react';
import { Card, CardBody, Badge, CustomInput } from 'reactstrap';
import { NavLink } from 'react-router-dom';
import classnames from 'classnames';

import { Colxx } from '../common/CustomBootstrap';
import { ContextMenuTrigger } from 'react-contextmenu';
import IntlMessages from '../../helpers/IntlMessages';

import { adminRoot } from '../../constants/defaultValues';

const PlineReportListItem = ({ item, handleCheckChange, isSelected, metrics, collect }) => {
  return (
    <Colxx xxs="12">
      <ContextMenuTrigger id="menu_id" data={item.id} collect={collect}>
        <Card
          onClick={(event) => handleCheckChange(event, item.id)}
          className={classnames('card d-flex mb-3', {
            active: isSelected,
          })}
        >
          <div className="d-flex flex-grow-1 min-width-zero">
            <CardBody className="align-self-center d-flex flex-column flex-md-row justify-content-between min-width-zero align-items-md-center">
              <NavLink
                to={`${adminRoot}/report/details/${item.id}`}
                id={`toggler${item.id}`}
                className="list-item-heading mb-0 truncate w-40 w-xs-100  mb-1 mt-1"
              >
                <i className="simple-icon-speedometer heading-icon" />
                <span className="align-middle d-inline-block">{item.pline_name}</span>
              </NavLink>
              <p className="mb-1 text-muted text-small w-15 w-xs-100">
                {new Date(item.created_at).toLocaleString()}
              </p>
              {item.execution_time !== null ?
                <p className="mb-1 text-muted text-small w-15 w-xs-100">
                  {item.execution_time}
                </p>
                :
                <div className="w-15 w-xs-100">
                  <Badge color={"danger"} pill>
                    <IntlMessages id="pline.error" />
                  </Badge>
                </div>
              }
            </CardBody>
            <div className="custom-control custom-checkbox pl-1 align-self-center mr-4">
              <CustomInput
                className="itemCheck mb-0"
                type="checkbox"
                id={`check_${item.id}`}
                checked={isSelected}
                onChange={(event) => handleCheckChange(event, item.id)}
                label=""
              />
            </div>
          </div>
          <div className="card-body pt-1">
            {metrics.length > 0 ?
              metrics.map((metric, index) => (
                <p
                  className="mb-0"
                  key={`metric_${metric.id}`}
                >
                  <span className="align-middle d-inline-block">
                    {`${metric.metric_name.toUpperCase()}`}
                  </span>
                  <span> </span>
                  <span className="align-middle d-inline-block text-muted">
                    {metric.score}
                  </span>
                </p>
              ))
              :
              ''
            }
          </div>
        </Card>
      </ContextMenuTrigger>
    </Colxx>
  );
};

/* React.memo detail : https://reactjs.org/docs/react-api.html#reactpurecomponent  */
export default React.memo(PlineReportListItem);
