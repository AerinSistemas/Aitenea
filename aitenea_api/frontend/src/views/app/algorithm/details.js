import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';

import {
  Row,
  Nav,
  NavItem,
  Button,
  DropdownToggle,
  DropdownItem,
  DropdownMenu,
  TabContent,
  TabPane,
  ButtonDropdown,
} from 'reactstrap';
import { NavLink, useParams } from 'react-router-dom';
import classnames from 'classnames';

import IntlMessages from '../../../helpers/IntlMessages';
import { Colxx } from '../../../components/common/CustomBootstrap';
import Breadcrumb from '../../../containers/navs/Breadcrumb';
import AlgorithmDetailsCard from '../../../components/applications/AlgorithmDetailsCard';
import SimpleDetailsPageHeading from '../../../containers/pages/SimpleDetailsPageHeading';

import {
  getAlgorithmDetails,
  selectedAlgorithmItemsChange,
} from '../../../redux/actions';


const AlgorithmDetails = ({
  match,
  loading,
  currentAlgorithm,
  selectedItems,
  selectedAlgorithmItemsChangeAction,
  getAlgorithmDetailsAction,
}) => {
  const { algorithmid } = useParams();
  const [activeTab, setActiveTab] = useState('details');

  useEffect(() => {
    selectedAlgorithmItemsChangeAction([parseInt(algorithmid)]);
  }, [selectedAlgorithmItemsChangeAction]);

  useEffect(() => {
    if (selectedItems.length > 0) {
      getAlgorithmDetailsAction();
    }
  }, [selectedItems]);

  return (
    <>
      <Row className="row">
        <Colxx xxs="12">
          <div className="disable-text-selection">
            <SimpleDetailsPageHeading
              heading="menu.algorithmdetails"
              match={match}
            />
          </div>
          {loading && currentAlgorithm != null ? (
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
                    <AlgorithmDetailsCard 
                      item={currentAlgorithm}
                    />
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

const mapStateToProps = ({ algorithmApp }) => {
  const {
    currentAlgorithm,
    selectedItems,
    loading
  } = algorithmApp;

  return {
    currentAlgorithm,
    selectedItems,
    loading,
  };
};

export default connect(mapStateToProps, {
  selectedAlgorithmItemsChangeAction: selectedAlgorithmItemsChange,
  getAlgorithmDetailsAction: getAlgorithmDetails,
})(AlgorithmDetails);
