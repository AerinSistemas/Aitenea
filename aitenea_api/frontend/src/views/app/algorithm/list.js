import React, { useState, useEffect } from 'react';

import { Row } from 'reactstrap';
import { Colxx } from '../../../components/common/CustomBootstrap'
import { injectIntl } from 'react-intl';
import { connect } from 'react-redux';
import {
  getAlgorithmList,
  getAlgorithmListWithOrder,
  getAlgorithmListSearch,
  changeAlgorithmListOrder
} from '../../../redux/actions';

import Pagination from '../../../containers/pages/Pagination';
import SimpleListPageHeading from '../../../containers/pages/SimpleListPageHeading';
import AlgorithmApplicationMenu from '../../../containers/applications/AlgorithmApplicationMenu';
import AlgorithmListItem from '../../../components/applications/AlgorithmListItem';

const chunk = (arr, size) => {
  let myArray = [];
  for (let i = 0; i < arr.length; i += size) {
    myArray.push(arr.slice(i, i + size));
  }
  return myArray;
};

const orderOptions = [
  { column: 'clas_name', label: 'Algorithm name' },
  { column: 'type', label: 'Algorithm type' },
];
const pageSizes = [4, 8, 12, 20];

const AlgorithmList = ({
  match,
  intl,
  loadingAlgorithm,
  algorithmItems,
  getAlgorithmListAction,
  getAlgorithmListSearchAction,
  getAlgorithmListWithOrderAction,
  changeAlgorithmListOrderAction,
  reload,
  orderDirection
}) => {

  const [currentPage, setCurrentPage] = useState(1);
  const [totalPage, setTotalPage] = useState(1);
  const [selectedPageSize, setSelectedPageSize] = useState(8);
  const [items, setItems] = useState([]);
  const [selectedOrderOption, setSelectedOrderOption] = useState({
    column: '',
    label: '',
  });

  useEffect(() => {
    setCurrentPage(1);
  }, [selectedPageSize, selectedOrderOption, reload]);

  useEffect(() => {
    document.body.classList.add('right-menu');
    getAlgorithmListAction();

    return () => {
      document.body.classList.remove('right-menu');
    };
  }, [reload]);

  useEffect(() => {
    if (loadingAlgorithm && algorithmItems != null) {
      setTotalPage(Math.ceil(algorithmItems.length / selectedPageSize));
      setItems(chunk(algorithmItems, selectedPageSize)[currentPage - 1]);
    }
  }, [algorithmItems, currentPage, selectedPageSize, selectedOrderOption]);

  const startIndex = (currentPage - 1) * selectedPageSize;
  const endIndex = currentPage * selectedPageSize;

  return (!loadingAlgorithm) ? (
    <div className="loading" />
  ) : (
    <>
      <Row className="app-row survey-app">
        <Colxx xxs="12">
          <div className="disable-text-selection">
            <SimpleListPageHeading
              heading="menu.algorithmlist"
              changeOrderBy={(column) => {
                setSelectedOrderOption(
                  orderOptions.find((x) => x.column === column)
                );
                getAlgorithmListWithOrderAction(column);
              }}
              changePageSize={setSelectedPageSize}
              selectedPageSize={selectedPageSize}
              totalItemCount={algorithmItems ? algorithmItems.length : 0}
              selectedOrderOption={selectedOrderOption}
              match={match}
              startIndex={startIndex}
              endIndex={endIndex}
              onSearchKey={(e) => {
                if (e.key === 'Enter') {
                  getAlgorithmListSearchAction(e.target.value);
                }
              }}
              orderOptions={orderOptions}
              pageSizes={pageSizes}
              handleOrderDirection={() => {
                changeAlgorithmListOrderAction()
              }}
            />
            <Row>
              {items != undefined ?
                orderDirection === "asc" ?
                  items.map((item, index) => (
                    <AlgorithmListItem
                      key={`algorithm_item_${item.id}`}
                      item={item}
                    />
                  ))
                  :
                  items.slice(0).reverse().map((item, index) => (
                    <AlgorithmListItem
                      key={`algorithm_item_${item.id}`}
                      item={item}
                    />
                  ))
                :
                ''
              }
              <Pagination
                currentPage={currentPage}
                totalPage={totalPage}
                onChangePage={(i) => setCurrentPage(i)}
              />
              <AlgorithmApplicationMenu />
            </Row>
          </div>
        </Colxx>
      </Row>
    </>
  );
};

const mapStateToProps = ({ algorithmApp }) => {
  const {
    algorithmItems,
    searchKeyword,
    orderDirection,
    orderColumn,
    orderColumns,
    reload
  } = algorithmApp;

  const loadingAlgorithm = algorithmApp.loading;

  return {
    algorithmItems,
    searchKeyword,
    orderDirection,
    orderColumn,
    orderColumns,
    loadingAlgorithm,
    reload
  };
};
export default injectIntl(
  connect(mapStateToProps, {
    getAlgorithmListAction: getAlgorithmList,
    getAlgorithmListWithOrderAction: getAlgorithmListWithOrder,
    getAlgorithmListSearchAction: getAlgorithmListSearch,
    changeAlgorithmListOrderAction: changeAlgorithmListOrder
  })(AlgorithmList)
);

