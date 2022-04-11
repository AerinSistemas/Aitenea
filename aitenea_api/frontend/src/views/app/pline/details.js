import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';

import {
  Row,
  Nav,
  NavItem,
  TabContent,
  TabPane,
} from 'reactstrap';
import { NavLink, useParams } from 'react-router-dom';
import classnames from 'classnames';

import IntlMessages from '../../../helpers/IntlMessages';
import { Colxx } from '../../../components/common/CustomBootstrap';
import PlineDetailsCard from '../../../components/applications/PlineDetailsCard';
import StepItem from '../../../components/applications/StepItem';
import SimplePlineReportListItem from '../../../components/applications/SimplePlineReportListItem';
import DeleteDetailsPageHeading from '../../../containers/pages/DeleteDetailsPageHeading';

import { adminRoot } from '../../../constants/defaultValues';

import {
  getPlineDetails,
  getStepListByPline,
  getPlineStatusListByPline,
  getPlineReportListByPline,
  getPlineReportMetricListByPline,
  deletePline,
  selectedPlineItemsChange,
} from '../../../redux/actions';


const PlineDetails = ({
  match,
  loadingPline,
  loadingStep,
  loadingReport,
  loadingMetric,
  loadingStatus,
  stepItems,
  currentPline,
  plineReportItems,
  plineStatusItems,
  plineReportMetricItems,
  selectedItems,
  selectedPlineItemsChangeAction,
  deletePlineAction,
  getPlineDetailsAction,
  getStepListByPlineAction,
  getPlineStatusListByPlineAction,
  getPlineReportListByPlineAction,
  getPlineReportMetricListByPlineAction
}) => {
  const { plineid } = useParams();
  const [activeTab, setActiveTab] = useState('details');

  useEffect(() => {
    selectedPlineItemsChangeAction([parseInt(plineid)]);
  }, [selectedPlineItemsChangeAction]);

  useEffect(() => {
    if (selectedItems.length > 0) {
      getPlineDetailsAction();
      getStepListByPlineAction();
      getPlineStatusListByPlineAction();
    }
  }, [selectedItems]);

  useEffect(() => {
    if (loadingPline && currentPline != null) {
      getPlineReportListByPlineAction();
      getPlineReportMetricListByPlineAction();
    }
  }, [currentPline]);

  return (
    <>
      <Row className="row">
        <Colxx xxs="12">
          <div className="disable-text-selection">
            <DeleteDetailsPageHeading
              heading="menu.plinedetails"
              match={match}
              handleDelete={() => {
                deletePlineAction();
              }}
            />
          </div>
          {loadingPline && loadingStep && loadingReport && loadingMetric && loadingStatus && currentPline != null ? (
            <>
              <Nav tabs className="separator-tabs ml-0 mb-5">
                <NavItem>
                  <NavLink
                    className={classnames({
                      active: activeTab === 'details',
                      'nav-link': true,
                    })}
                    location={{}}
                    to="#"
                    onClick={() => setActiveTab('details')}
                  >
                    <IntlMessages id="menu.details" />
                  </NavLink>
                </NavItem>
                <NavItem>
                  <NavLink
                    location={{}}
                    to="#"
                    className={classnames({
                      active: activeTab === 'reports',
                      'nav-link': true,
                    })}
                    onClick={() => setActiveTab('reports')}
                  >
                    <IntlMessages id="menu.reports" />
                  </NavLink>
                </NavItem>
              </Nav>

              <TabContent activeTab={activeTab}>
                <TabPane tabId="details">
                  <Row>
                    <PlineDetailsCard 
                      item={currentPline}
                      status={
                        plineStatusItems.find(obj => {
                          return obj.pline === currentPline.id
                        })
                      }
                    />
                    <Colxx xxs="12" lg="8">
                      <ul className="list-unstyled mb-4">
                        {stepItems != undefined ?
                          stepItems.map((item, index) => (
                            <li data-id={item.id} key={item.id}>
                              <StepItem
                                key={`step_item_${item.id}`}
                                item={item}
                                expanded={!item.step_name && true}
                              />
                            </li>
                          ))
                          :
                          ''
                        }
                      </ul>
                    </Colxx>
                  </Row>
                </TabPane>
                <TabPane tabId="reports">
                  <Row>
                    {plineReportItems != undefined ?
                      plineReportItems.slice(0).sort(function(a, b) {
                        if (a.created_at > b.created_at) return -1;
                        if (a.created_at < b.created_at) return 1;
                        return 0;
                        }).map((item, index) => (
                        <SimplePlineReportListItem
                          key={`pline_report_item_${item.id}`}
                          item={item}
                          metrics={
                            plineReportMetricItems.filter(obj => {
                              return obj.pline_report === item.id
                            })
                          }
                        />
                      ))
                      :
                      ''
                    }
                  </Row>
                </TabPane>
              </TabContent>
            </>
          ) : (
            <div className="loading" />
          )}
        </Colxx>
      </Row>
    </>
  );
};

const mapStateToProps = ({ plineApp, reportsApp }) => {
  const {
    currentPline,
    selectedItems,
    stepItems,
  } = plineApp;


  const {
    plineReportItems,
    plineStatusItems,
    plineReportMetricItems,
  } = reportsApp;

  const loadingPline = plineApp.loading;
  const loadingReport = reportsApp.loading;
  const loadingStep = plineApp.loadingStep;
  const loadingMetric = reportsApp.loadingMetric;
  const loadingStatus = reportsApp.loadingStatus;

  return {
    currentPline,
    stepItems,
    plineReportItems,
    plineStatusItems,
    plineReportMetricItems,
    selectedItems,
    loadingPline,
    loadingStep,
    loadingReport,
    loadingMetric,
    loadingStatus
  };
};

export default connect(mapStateToProps, {
  deletePlineAction: deletePline,
  selectedPlineItemsChangeAction: selectedPlineItemsChange,
  getPlineDetailsAction: getPlineDetails,
  getStepListByPlineAction: getStepListByPline,
  getPlineStatusListByPlineAction: getPlineStatusListByPline,
  getPlineReportListByPlineAction: getPlineReportListByPline,
  getPlineReportMetricListByPlineAction: getPlineReportMetricListByPline
})(PlineDetails);
