import React from 'react';
import { Card, CustomInput, Badge } from 'reactstrap';
import { NavLink } from 'react-router-dom';
import classnames from 'classnames';
import { Colxx } from '../../components/common/CustomBootstrap';
import IntlMessages from '../../helpers/IntlMessages';

import { adminRoot } from '../../constants/defaultValues';

const AlgorithmListItem = ({ item }) => {
  return (
    <Colxx xxs="12" key={item.id} className="mb-3">
      <Card className="d-flex flex-row">
        <NavLink  
          to={`${adminRoot}/algorithm/details/${item.id}`}
          className="d-flex"
        >
          <img
            alt="algorithm_thumbnail"
            src={
              item.type.includes("aitenea") ? 
                "../../../static/assets/logos/mobile.svg"
              :
              "../../../static/assets/logos/mobile.svg"
            }
            className="list-thumbnail responsive border-0 card-img-left"
          />
        </NavLink>
        <div className="pl-2 d-flex flex-grow-1 min-width-zero">
          <div className="card-body align-self-center d-flex flex-column flex-lg-row justify-content-between min-width-zero align-items-lg-center">
            <NavLink 
              to={`${adminRoot}/algorithm/details/${item.id}`}
              className="w-40 w-sm-100"
            >
              <p className="list-item-heading mb-1 truncate">
                {item.class_name}
              </p>
            </NavLink>
            <div className="w-15 w-sm-100">
              {item.type.includes("aitenea")  ?
                <Badge color={"outline-info"} pill>
                  <IntlMessages id={`algorithm.${item.type}`} />
                </Badge>
                :
                <Badge color={"outline-dark"} pill>
                  <IntlMessages id={`algorithm.${item.type}`} />
                </Badge>
              }
            </div>
          </div>
        </div>
      </Card>
    </Colxx>
  );
};

/* React.memo detail : https://reactjs.org/docs/react-api.html#reactpurecomponent  */
export default React.memo(AlgorithmListItem);