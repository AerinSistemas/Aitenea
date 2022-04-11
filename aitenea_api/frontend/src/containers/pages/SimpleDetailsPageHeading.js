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

const SimpleDetailsPageHeading = ({
  intl,
  match,
  heading,
}) => {
  const { messages } = intl;

  return (
    <Row>
      <Colxx xxs="12">
        <div className="mb-2">
          <h1>
            <IntlMessages id={heading} />
          </h1>

          <Breadcrumb match={match} />
        </div>
      </Colxx>
    </Row>
  );
};

export default injectIntl(SimpleDetailsPageHeading);
