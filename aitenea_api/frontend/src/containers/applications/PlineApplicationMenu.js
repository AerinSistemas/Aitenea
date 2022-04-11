/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable react/no-array-index-key */
import React from 'react';
import { connect } from 'react-redux';
import { NavItem } from 'reactstrap';
import { NavLink } from 'react-router-dom';
import PerfectScrollbar from 'react-perfect-scrollbar';
import classnames from 'classnames';

import IntlMessages from '../../helpers/IntlMessages';
import ApplicationMenu from '../../components/common/ApplicationMenu';
import { getPlineListWithFilter } from '../../redux/actions';

const PlineApplicationMenu = ({
  plineItems,
  filter,
  allPlineItems,
  loading,
  getPlineListWithFilterAction,
}) => {
  const addFilter = (column, value) => {
    getPlineListWithFilterAction(column, value);
  };

  return (
    <ApplicationMenu>
      <PerfectScrollbar
        options={{ suppressScrollX: true, wheelPropagation: false }}
      >
        <div className="p-4">
          <p className="text-muted text-small">
            <IntlMessages id="pline.status" />
          </p>
          <ul className="list-unstyled mb-5">
            <NavItem className={classnames({ active: !filter })}>
              <NavLink to="#" onClick={() => addFilter('', '')} location={{}}>
                <i className="simple-icon-reload" />
                <IntlMessages id="pline.all-plines" />
                <span className="float-right">
                  {loading && allPlineItems.length}
                </span>
              </NavLink>
            </NavItem>
            <NavItem
              className={classnames({
                active:
                  filter &&
                  filter.column === 'fitted' &&
                  filter.value === false,
              })}
            >
              <NavLink
                location={{}}
                to="#"
                onClick={() => addFilter('fitted', false)}
              >
                <i className="simple-icon-close" />
                <IntlMessages id="pline.not-fitted-plines" />
                <span className="float-right">
                  {loading &&
                    plineItems.filter((x) => x.fitted === false).length}
                </span>
              </NavLink>
            </NavItem>
            <NavItem
              className={classnames({
                active:
                  filter &&
                  filter.column === 'fitted' &&
                  filter.value === true,
              })}
            >
              <NavLink
                to="#"
                location={{}}
                onClick={() => addFilter('fitted', true)}
              >
                <i className="simple-icon-check" />
                <IntlMessages id="pline.fitted-plines" />
                <span className="float-right">
                  {loading &&
                    plineItems.filter((x) => x.fitted === true).length}
                </span>
              </NavLink>
            </NavItem>
          </ul>
        </div>
      </PerfectScrollbar>
    </ApplicationMenu>
  );
};

const mapStateToProps = ({ plineApp }) => {
  const {
    plineItems,
    filter,
    allPlineItems,
    loading,
  } = plineApp;

  return {
    plineItems,
    filter,
    allPlineItems,
    loading,
  };
};
export default connect(mapStateToProps, {
  getPlineListWithFilterAction: getPlineListWithFilter,
})(PlineApplicationMenu);
