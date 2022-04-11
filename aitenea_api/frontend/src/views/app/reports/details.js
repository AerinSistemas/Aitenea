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
import PlineReportDetailsCard from '../../../components/applications/PlineReportDetailsCard';
import PlineReportMetricItem from '../../../components/applications/PlineReportMetricItem';
import DeleteDetailsPageHeading from '../../../containers/pages/DeleteDetailsPageHeading';

import { adminRoot } from '../../../constants/defaultValues';

import {
  getPlineReportDetails,
  getPlineReportMetricListByPlineReport,
  deletePlineReport,
  selectedPlineReportItemsChange,
} from '../../../redux/actions';


const ReportDetails = ({
  match,
  loadingReport,
  loadingMetric,
  currentPlineReport,
  plineReportMetricItems,
  selectedItems,
  selectedPlineReportItemsChangeAction,
  deletePlineReportAction,
  getPlineReportDetailsAction,
  getPlineReportMetricListByPlineReportAction
}) => {
  const { reportid } = useParams();
  const [activeTab, setActiveTab] = useState('details');

  useEffect(() => {
    selectedPlineReportItemsChangeAction([parseInt(reportid)]);
  }, [selectedPlineReportItemsChangeAction]);

  useEffect(() => {
    if (selectedItems.length > 0) {
      getPlineReportDetailsAction();
    }
  }, [selectedItems]);

  useEffect(() => {
    if (loadingReport && currentPlineReport != null) {
      getPlineReportMetricListByPlineReportAction();
    }
  }, [currentPlineReport]);

  return (
    <>
      <Row className="row">
        <Colxx xxs="12">
          <div className="disable-text-selection">
            <DeleteDetailsPageHeading
              heading="menu.reportdetails"
              match={match}
              handleDelete={() => {
                deletePlineReportAction();
              }}
            />
          </div>
          {loadingReport && loadingMetric && currentPlineReport != null ? (
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
              </Nav>

              <TabContent activeTab={activeTab}>
                <TabPane tabId="details">
                  <Row>
                    <PlineReportDetailsCard 
                      item={currentPlineReport}
                    />
                    <Colxx xxs="12" lg="6">
                      <ul className="list-unstyled mb-4">
                        {plineReportMetricItems != undefined ?
                          plineReportMetricItems.map((item, index) => (
                            <li data-id={item.id} key={item.id}>
                              <PlineReportMetricItem
                                key={`metric_item_${item.id}`}
                                item={item}
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

const mapStateToProps = ({ reportsApp }) => {
  const {
    currentPlineReport,
    plineReportItems,
    plineReportMetricItems,
    selectedItems
  } = reportsApp;

  const loadingReport = reportsApp.loading;
  const loadingMetric = reportsApp.loadingMetric;

  return {
    currentPlineReport,
    plineReportItems,
    plineReportMetricItems,
    selectedItems,
    loadingReport,
    loadingMetric,
  };
};

export default connect(mapStateToProps, {
  deletePlineReportAction: deletePlineReport,
  selectedPlineReportItemsChangeAction: selectedPlineReportItemsChange,
  getPlineReportDetailsAction: getPlineReportDetails,
  getPlineReportMetricListByPlineReportAction: getPlineReportMetricListByPlineReport
})(ReportDetails);
