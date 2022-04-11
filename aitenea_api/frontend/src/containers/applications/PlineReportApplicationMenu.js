/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-static-element-interactions */
/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable jsx-a11y/label-has-for */
/* eslint-disable react/no-array-index-key */
import React from 'react';
import { connect } from 'react-redux';
import { NavItem, Row } from 'reactstrap';
import { NavLink } from 'react-router-dom';
import PerfectScrollbar from 'react-perfect-scrollbar';
import classnames from 'classnames';

import { Colxx } from '../../components/common/CustomBootstrap';
//import {
//  DecimalRangeTooltip,
//} from '../../components/common/SliderTooltips';

import IntlMessages from '../../helpers/IntlMessages';
import ApplicationMenu from '../../components/common/ApplicationMenu';
import { getPlineReportListWithFilter } from '../../redux/actions';

const PlineReportApplicationMenu = ({
  plineReportItems,
  filter,
  allPlineReportItems,
  loading,
  getPlineReportListWithFilterAction,
}) => {
  const addFilter = (column, value) => {
    getPlineReportListWithFilterAction(column, value);
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
                <IntlMessages id="reports.all-reports" />
                <span className="float-right">
                  {loading && allPlineReportItems.length}
                </span>
              </NavLink>
            </NavItem>

            <NavItem
              className={classnames({
                active:
                  filter &&
                  filter.column === 'score' &&
                  filter.value === false,
              })}
            >
              <NavLink
                location={{}}
                to="#"
                onClick={() => addFilter('fitted', false)}
              >
                <i className="simple-icon-close" />
                <IntlMessages id="reports.score-range" />
                <span className="float-right">
                  {/*loading &&
                    plineReportItems.filter((x) => x.fitted === false).length*/}
                </span>
              </NavLink>
              {/*
              <Row>
                <Colxx xxs="12" sm="12">
                  <label>
                    <IntlMessages id="reports.score-range" />
                  </label>
                  <DecimalRangeTooltip
                    min={0}
                    max={100}
                    className="mb-5"
                    defaultValue={[80, 100]}
                    allowCross={false}
                    pushable={10}
                  />
                </Colxx>
              </Row>
              */}
            </NavItem>
          </ul>
        </div>
        
        <div className="p-4">
          <p className="text-muted text-small">
            <IntlMessages id="pline.status" />
          </p>
          <ul className="list-unstyled mb-5">
            
            <NavItem className={classnames({ active: !filter })}>
              <NavLink to="#" onClick={() => addFilter('', '')} location={{}}>
                <i className="simple-icon-reload" />
                <IntlMessages id="reports.all-reports" />
                <span className="float-right">
                  {loading && allPlineReportItems.length}
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
                <IntlMessages id="reports.score-range" />
                <span className="float-right">
                  {/*loading &&
                      plineReportItems.filter((x) => x.fitted === false).length*/}
                </span>
              </NavLink>
            </NavItem>
          </ul>
        </div>
      </PerfectScrollbar>
    </ApplicationMenu>
  );
};

const mapStateToProps = ({ reportsApp }) => {
  const {
    plineReportItems,
    filter,
    allPlineReportItems,
    loading,
  } = reportsApp;

  return {
    plineReportItems,
    filter,
    allPlineReportItems,
    loading,
  };
};
export default connect(mapStateToProps, {
  getPlineReportListWithFilterAction: getPlineReportListWithFilter,
})(PlineReportApplicationMenu);
