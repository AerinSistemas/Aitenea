import React, { useState, useEffect } from 'react';

import { Row } from 'reactstrap';
import { Colxx } from '../../../components/common/CustomBootstrap'
import { injectIntl } from 'react-intl';
import { connect } from 'react-redux';
import {
  getPlineList,
  getPlineListWithOrder,
  getPlineListSearch,
  selectedPlineItemsChange,
  getPlineStatusList,
  deletePline,
  changePlineListOrder
} from '../../../redux/actions';

import Pagination from '../../../containers/pages/Pagination';
import DeleteListPageHeading from '../../../containers/pages/DeleteListPageHeading';
import PlineApplicationMenu from '../../../containers/applications/PlineApplicationMenu';
import PlineListItem from '../../../components/applications/PlineListItem';
import ContextMenuContainer from '../../../containers/pages/ContextMenuContainer';

const chunk = (arr, size) => {
  let myArray = [];
  for (let i = 0; i < arr.length; i += size) {
    myArray.push(arr.slice(i, i + size));
  }
  return myArray;
};

const orderOptions = [
  { column: 'name', label: 'Pline name' },
  { column: 'creation_timestamp', label: 'Creation date' }
];
const pageSizes = [4, 8, 12, 20];

function collect(props) {
  return { data: props.data };
}

const PlineList = ({
  match,
  intl,
  loadingPline,
  loadingStatus,
  plineItems,
  plineStatusItems,
  selectedItems,
  getPlineListAction,
  selectedPlineItemsChangeAction,
  getPlineStatusListAction,
  getPlineListSearchAction,
  getPlineListWithOrderAction,
  deletePlineAction,
  changePlineListOrderAction,
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
    selectedPlineItemsChangeAction([]);
    getPlineListAction();
    getPlineStatusListAction();

    return () => {
      document.body.classList.remove('right-menu');
    };
  }, [reload]);

  useEffect(() => {
    if (loadingPline && plineItems != null) {
      setTotalPage(Math.ceil(plineItems.length / selectedPageSize));
      setItems(chunk(plineItems, selectedPageSize)[currentPage - 1]);
    }
  }, [plineItems, currentPage, selectedPageSize, selectedOrderOption]);

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
    selectedPlineItemsChangeAction(selectedList);
    document.activeElement.blur();
  };

  const handleChangeSelectAll = () => {
    if (loadingPline) {
      if (selectedItems.length >= items.length) {
        selectedPlineItemsChangeAction([]);
      } else {
        selectedPlineItemsChangeAction(items.map((x) => x.id));
      }
      document.activeElement.blur();
    }
  };

  const onContextMenuClick = (e, data) => {
    if (data.action == "delete") {
      deletePlineAction();
    }
  };

  const onContextMenu = (e, data) => {
    const clickedItemId = data.data;
    if (!selectedItems.includes(clickedItemId)) {
      selectedPlineItemsChangeAction([clickedItemId]);
    }

    return true;
  };

  const startIndex = (currentPage - 1) * selectedPageSize;
  const endIndex = currentPage * selectedPageSize;

  return (!loadingPline || !loadingStatus) ? (
    <div className="loading" />
  ) : (
    <>
      <Row className="app-row survey-app">
        <Colxx xxs="12">
          <div className="disable-text-selection">
            <DeleteListPageHeading
              heading="menu.plinelist"
              handleChangeSelectAll={handleChangeSelectAll}
              changeOrderBy={(column) => {
                setSelectedOrderOption(
                  orderOptions.find((x) => x.column === column)
                );
                getPlineListWithOrderAction(column);
              }}
              changePageSize={setSelectedPageSize}
              selectedPageSize={selectedPageSize}
              totalItemCount={plineItems ? plineItems.length : 0}
              selectedOrderOption={selectedOrderOption}
              match={match}
              startIndex={startIndex}
              endIndex={endIndex}
              selectedItemsLength={selectedItems ? selectedItems.length : 0}
              itemsLength={items ? items.length : 0}
              onSearchKey={(e) => {
                if (e.key === 'Enter') {
                  getPlineListSearchAction(e.target.value);
                }
              }}
              orderOptions={orderOptions}
              pageSizes={pageSizes}
              handleDelete={() => {
                deletePlineAction()
              }}
              handleOrderDirection={() => {
                changePlineListOrderAction()
              }}
            />
            <Row>
              {items != undefined ?
                orderDirection === "asc" ?
                  items.map((item, index) => (
                    <PlineListItem
                      key={`pline_item_${item.id}`}
                      item={item}
                      handleCheckChange={handleCheckChange}
                      isSelected={loadingPline ? selectedItems.includes(item.id) : false}
                      status={
                        plineStatusItems.find(obj => {
                          return obj.pline === item.id
                        })
                      }
                      collect={collect}
                    />
                  ))
                  :
                  items.slice(0).reverse().map((item, index) => (
                    <PlineListItem
                      key={`pline_item_${item.id}`}
                      item={item}
                      handleCheckChange={handleCheckChange}
                      isSelected={loadingPline ? selectedItems.includes(item.id) : false}
                      status={
                        plineStatusItems.find(obj => {
                          return obj.pline === item.id
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
      <PlineApplicationMenu />
      <ContextMenuContainer
        onContextMenuClick={onContextMenuClick}
        onContextMenu={onContextMenu}
      />
    </>
  );
};

const mapStateToProps = ({ plineApp, reportsApp }) => {
  const {
    plineItems,
    searchKeyword,
    orderDirection,
    orderColumn,
    orderColumns,
    selectedItems,
    reload
  } = plineApp;

  const {
    plineStatusItems,
  } = reportsApp;

  const loadingPline = plineApp.loading;
  const loadingStatus = reportsApp.loadingStatus;

  return {
    plineItems,
    searchKeyword,
    orderDirection,
    orderColumn,
    orderColumns,
    selectedItems,
    plineStatusItems,
    loadingPline,
    loadingStatus,
    reload
  };
};
export default injectIntl(
  connect(mapStateToProps, {
    getPlineListAction: getPlineList,
    getPlineListWithOrderAction: getPlineListWithOrder,
    getPlineListSearchAction: getPlineListSearch,
    selectedPlineItemsChangeAction: selectedPlineItemsChange,
    getPlineStatusListAction: getPlineStatusList,
    deletePlineAction: deletePline,
    changePlineListOrderAction: changePlineListOrder
  })(PlineList)
);

