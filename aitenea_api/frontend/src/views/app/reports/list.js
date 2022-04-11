import React, { useState, useEffect } from 'react';

import { Row } from 'reactstrap';
import { Colxx } from '../../../components/common/CustomBootstrap'
import { injectIntl } from 'react-intl';
import { connect } from 'react-redux';
import {
  getPlineReportList,
  getPlineReportListWithOrder,
  getPlineReportListSearch,
  selectedPlineReportItemsChange,
  deletePlineReport,
  changePlineReportListOrder,
  getPlineReportMetricList,
} from '../../../redux/actions';

import Pagination from '../../../containers/pages/Pagination';
import DeleteListPageHeading from '../../../containers/pages/DeleteListPageHeading';
import PlineReportListItem from '../../../components/applications/PlineReportListItem';
import ContextMenuContainer from '../../../containers/pages/ContextMenuContainer';

const chunk = (arr, size) => {
  let myArray = [];
  for (let i = 0; i < arr.length; i += size) {
    myArray.push(arr.slice(i, i + size));
  }
  return myArray;
};

const orderOptions = [
  { column: 'pline_name', label: 'Pline name' },
  { column: 'creation_timestamp', label: 'Creation date' },
  { column: 'execution_time', label: 'Execution time' },
  { column: 'score', label: 'Score' }
];
const pageSizes = [4, 8, 12, 20];

function collect(props) {
  return { data: props.data };
}

const PlineReportList = ({
  match,
  intl,
  loadingReport,
  loadingMetric,
  plineReportItems,
  plineReportMetricItems,
  selectedItems,
  getPlineReportListAction,
  selectedPlineReportItemsChangeAction,
  getPlineReportListSearchAction,
  getPlineReportListWithOrderAction,
  deletePlineReportAction,
  changePlineReportListOrderAction,
  getPlineReportMetricListAction,
  reload,
  orderDirection
}) => {
  
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPage, setTotalPage] = useState(1);
  const [selectedPageSize, setSelectedPageSize] = useState(8);
  const [lastChecked, setLastChecked] = useState(null);
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
    selectedPlineReportItemsChangeAction([]);
    getPlineReportListAction();
    getPlineReportMetricListAction();

    return () => {
      document.body.classList.remove('right-menu');
    };
  }, [reload]);

  useEffect(() => {
    if (loadingReport && plineReportItems != null) {
      setTotalPage(Math.ceil(plineReportItems.length / selectedPageSize));
      setItems(chunk(plineReportItems, selectedPageSize)[currentPage - 1]);
    }
  }, [plineReportItems, currentPage, selectedPageSize, selectedOrderOption]);

  const handleCheckChange = (event, id) => {
    if (lastChecked == null) {
      setLastChecked(id);
    }

    let selectedList = Object.assign([], selectedItems);
    if (selectedList.includes(id)) {
      selectedList = selectedList.filter((x) => x !== id);
    } else {
      selectedList.push(id);
    }
    selectedPlineReportItemsChangeAction(selectedList);
    document.activeElement.blur();
  };

  const handleChangeSelectAll = () => {
    if (loadingReport) {
      if (selectedItems.length >= items.length) {
        selectedPlineReportItemsChangeAction([]);
      } else {
        selectedPlineReportItemsChangeAction(items.map((x) => x.id));
      }
      document.activeElement.blur();
    }
  };

  const onContextMenuClick = (e, data) => {
    if (data.action == "delete") {
      deletePlineReportAction();
    }
  };

  const onContextMenu = (e, data) => {
    const clickedItemId = data.data;
    if (!selectedItems.includes(clickedItemId)) {
      selectedPlineReportItemsChangeAction([clickedItemId]);
    }

    return true;
  };

  const startIndex = (currentPage - 1) * selectedPageSize;
  const endIndex = currentPage * selectedPageSize;

  return (!loadingReport || !loadingMetric) ? (
    <div className="loading" />
  ) : (
    <>
      <Row className="app-row survey-app">
        <Colxx xxs="12">
          <div className="disable-text-selection">
            <DeleteListPageHeading
              heading="menu.reportlist"
              handleChangeSelectAll={handleChangeSelectAll}
              changeOrderBy={(column) => {
                setSelectedOrderOption(
                  orderOptions.find((x) => x.column === column)
                );
                getPlineReportListWithOrderAction(column);
              }}
              changePageSize={setSelectedPageSize}
              selectedPageSize={selectedPageSize}
              totalItemCount={plineReportItems ? plineReportItems.length: 0}
              selectedOrderOption={selectedOrderOption}
              match={match}
              startIndex={startIndex}
              endIndex={endIndex}
              selectedItemsLength={selectedItems ? selectedItems.length : 0}
              itemsLength={items ? items.length : 0}
              onSearchKey={(e) => {
                if (e.key === 'Enter') {
                  getPlineReportListSearchAction(e.target.value);
                }
              }}
              orderOptions={orderOptions}
              pageSizes={pageSizes}
              handleDelete={() => {
                deletePlineReportAction()
              }}
              handleOrderDirection={() => {
                changePlineReportListOrderAction()
              }}
            />
            <Row>
              {items !== undefined ?
                orderDirection === "asc" ?
                  items.map((item, index) => (
                    <PlineReportListItem
                      key={`pline_item_${item.id}`}
                      item={item}
                      handleCheckChange={handleCheckChange}
                      isSelected={loadingReport ? selectedItems.includes(item.id) : false}
                      metrics={
                        plineReportMetricItems.filter(obj => {
                          return obj.pline_report === item.id
                        })
                      }
                      collect={collect}
                    />
                  ))
                  :
                  items.slice(0).reverse().map((item, index) => (
                    <PlineReportListItem
                      key={`pline_item_${item.id}`}
                      item={item}
                      handleCheckChange={handleCheckChange}
                      isSelected={loadingReport ? selectedItems.includes(item.id) : false}
                      metrics={
                        plineReportMetricItems.filter(obj => {
                          return obj.pline_report === item.id
                        })
                      }
                      collect={collect}
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
            </Row>
          </div>
        </Colxx>
      </Row>
      <ContextMenuContainer
        onContextMenuClick={onContextMenuClick}
        onContextMenu={onContextMenu}
      />
    </>
  );
};

const mapStateToProps = ({ reportsApp }) => {
  const {
    plineReportItems,
    plineReportMetricItems,
    searchKeyword,
    orderDirection,
    orderColumn,
    orderColumns,
    selectedItems,
    reload
  } = reportsApp;

  const loadingReport = reportsApp.loading;
  const loadingMetric = reportsApp.loadingMetric;

  return {
    plineReportItems,
    plineReportMetricItems,
    searchKeyword,
    orderDirection,
    orderColumn,
    orderColumns,
    selectedItems,
    loadingReport,
    loadingMetric,
    reload
  };
};
export default injectIntl(
  connect(mapStateToProps, {
    getPlineReportListAction: getPlineReportList,
    getPlineReportListWithOrderAction: getPlineReportListWithOrder,
    getPlineReportListSearchAction: getPlineReportListSearch,
    selectedPlineReportItemsChangeAction: selectedPlineReportItemsChange,
    deletePlineReportAction: deletePlineReport,
    changePlineReportListOrderAction: changePlineReportListOrder,
    getPlineReportMetricListAction: getPlineReportMetricList,
  })(PlineReportList)
);

