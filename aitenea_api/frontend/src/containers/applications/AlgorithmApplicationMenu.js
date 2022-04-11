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
import { getAlgorithmListWithFilter } from '../../redux/actions';

const AlgorithmApplicationMenu = ({
  algorithmItems,
  filter,
  allAlgorithmItems,
  loading,
  getAlgorithmListWithFilterAction,
}) => {
  const addFilter = (column, value) => {
    getAlgorithmListWithFilterAction(column, value);
  };

  return (
    <ApplicationMenu>
      <PerfectScrollbar
        options={{ suppressScrollX: true, wheelPropagation: false }}
      >
        <div className="p-4">
          <p className="text-muted text-small">
            <IntlMessages id="menu.algorithms" />
          </p>
          <ul className="list-unstyled mb-5">
            <NavItem className={classnames({ active: !filter })}>
              <NavLink to="#" onClick={() => addFilter('', '')} location={{}}>
                <i className="simple-icon-reload" />
                <IntlMessages id="algorithm.all-algorithms" />
                <span className="float-right">
                  {loading && allAlgorithmItems.length}
                </span>
              </NavLink>
            </NavItem>

            <NavItem
              className={classnames({
                active:
                  filter &&
                  filter.column === 'type' &&
                  filter.value === "aitenea_ai",
              })}
            >
              <NavLink
                location={{}}
                to="#"
                onClick={() => addFilter('type', "aitenea_ai")}
              >
                <i className="simple-icon-check" />
                <IntlMessages id="algorithm.aitenea_ai" />
                <span className="float-right">
                  {loading &&
                    algorithmItems.filter((x) => x.type === "aitenea_ai").length}
                </span>
              </NavLink>
            </NavItem>

            <NavItem
              className={classnames({
                active:
                  filter &&
                  filter.column === 'type' &&
                  filter.value === "aitenea_transform",
              })}
            >
              <NavLink
                to="#"
                location={{}}
                onClick={() => addFilter('type', "aitenea_transform")}
              >
                <i className="simple-icon-check" />
                <IntlMessages id="algorithm.aitenea_transform" />
                <span className="float-right">
                  {loading &&
                    algorithmItems.filter((x) => x.type === "aitenea_transform").length}
                </span>
              </NavLink>
            </NavItem>

            <NavItem
              className={classnames({
                active:
                  filter &&
                  filter.column === 'type' &&
                  filter.value === "external_ai",
              })}
            >
              <NavLink
                to="#"
                location={{}}
                onClick={() => addFilter('type', "external_ai")}
              >
                <i className="simple-icon-check" />
                <IntlMessages id="algorithm.external_ai" />
                <span className="float-right">
                  {loading &&
                    algorithmItems.filter((x) => x.type === "external_ai").length}
                </span>
              </NavLink>
            </NavItem>

            <NavItem
              className={classnames({
                active:
                  filter &&
                  filter.column === 'type' &&
                  filter.value === "external_transform",
              })}
            >
              <NavLink
                to="#"
                location={{}}
                onClick={() => addFilter('type', "external_transform")}
              >
                <i className="simple-icon-check" />
                <IntlMessages id="algorithm.external_transform" />
                <span className="float-right">
                  {loading &&
                    algorithmItems.filter((x) => x.type === "external_transform").length}
                </span>
              </NavLink>
            </NavItem>
          </ul>
        </div>
      </PerfectScrollbar>
    </ApplicationMenu>
  );
};

const mapStateToProps = ({ algorithmApp }) => {
  const {
    algorithmItems,
    filter,
    allAlgorithmItems,
    loading,
  } = algorithmApp;

  return {
    algorithmItems,
    filter,
    allAlgorithmItems,
    loading,
  };
};
export default connect(mapStateToProps, {
  getAlgorithmListWithFilterAction: getAlgorithmListWithFilter,
})(AlgorithmApplicationMenu);
