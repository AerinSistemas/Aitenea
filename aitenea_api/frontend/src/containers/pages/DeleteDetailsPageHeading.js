/* eslint-disable react/no-array-index-key */
import React, { useState } from 'react';
import {
  Row,
  Button,
  ButtonDropdown,
  UncontrolledDropdown,
  DropdownMenu,
  DropdownItem,
  DropdownToggle,
  CustomInput,
  Collapse,
} from 'reactstrap';
import { injectIntl } from 'react-intl';

import { Colxx, Separator } from '../../components/common/CustomBootstrap';
import Breadcrumb from '../navs/Breadcrumb';
import IntlMessages from '../../helpers/IntlMessages';

const DeleteDetailsPageHeading = ({
  intl,
  match,
  heading,
  handleDelete,
}) => {
  const [dropdownSplitOpen, setDropdownSplitOpen] = useState(false);
  const { messages } = intl;

  return (
    <Row>
      <Colxx xxs="12">
        <div className="mb-2">
          <h1>
            <IntlMessages id={heading} />
          </h1>

          <div className="text-zero top-right-button-container">
            {'  '}
            <ButtonDropdown
              isOpen={dropdownSplitOpen}
              toggle={() => setDropdownSplitOpen(!dropdownSplitOpen)}
            >
              <DropdownToggle
                caret
                color="primary"
                className="dropdown-toggle-split btn-lg"
              >
                <IntlMessages id="pages.actions" />
              </DropdownToggle>
              <DropdownMenu right>
                <DropdownItem
                  onClick={() => handleDelete()}
                >
                  <IntlMessages id="pages.delete" />
                </DropdownItem>
              </DropdownMenu>
            </ButtonDropdown>
          </div>
          <Breadcrumb match={match} />
        </div>
      </Colxx>
    </Row>
  );
};

export default injectIntl(DeleteDetailsPageHeading);
