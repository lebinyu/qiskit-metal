# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
Module containing Net information storage.
"""
#from typing import Tuple
import pandas as pd
from .. import logger


class QNet():
    """
    Use DataFrame to hold Net Information about the connected pins of a design.   
    There is one uniqe net_id for each connected pin.
    """

    def __init__(self):
        """ Hold the net information of all the USED pins within a design."""
        self.column_names = ['net_id', 'component_id', 'pin_name']
        self._net_info = pd.DataFrame(columns=self.column_names)
        self._qnet_latest_assigned_id = 0
        self.logger = logger  # type: logging.Logger

    def _get_new_net_id(self) -> int:
        """ Provide uniqe new qnet_id.

        Returns:
            int: ID to use for storing a new net within _net_info.
        """
        self._qnet_latest_assigned_id += 1
        return self._qnet_latest_assigned_id

    @property
    def qnet_latest_assigned_id(self) -> int:
        """Return unique number for each net in table.

        Returns:
            int: For user of the design class to know the lastest id added to _net_info.
        """
        return self._qnet_latest_assigned_id

    @property
    def net_info(self) -> pd.DataFrame:
        """Provide table of all nets within the design.

        Returns:
            pd.DataFrame: Table of the net of pins within design.
        """
        return self._net_info

    def add_pins_to_table(self, comp1_id: int, pin1_name: str, comp2_id: int,
                          pin2_name: str) -> int:
        """Add two entries into the _net_info table. If either component/pin is already in net_info,
        the connection will NOT be added to the net_info.

        Arguments:
            comp1_id (int): Name of component 1. 
            pin1_name (str): Corresponding pin name for component1.
            comp2_id (int): Name of component 2.
            pint2 (str): Corresponding pin name for component2.

        Returns:
            int: 0 if not added to list, otherwise the netid
        """
        net_id = 0  # Zero mean false, the pin was not added to _net_info

        if not isinstance(comp1_id, int):
            self.logger.warning(
                f'Expected an int, but have {comp1_id}. The pins are were not entered to the net_info table.'
            )
            return net_id
        if not isinstance(comp2_id, int):
            self.logger.warning(
                f'Expected an int, but have {comp2_id}. The pins are were not entered to the net_info table.'
            )
            return net_id
        if not isinstance(pin1_name, str):
            self.logger.warning(
                f'Expected a string, but have {pin1_name}. The pins are were not entered to the net_info table.'
            )
            return net_id
        if not isinstance(pin2_name, str):
            self.logger.warning(
                f'Expected a string, but have {pin2_name}. The pins are were not entered to the net_info table.'
            )
            return net_id

        # Confirm the component-pin combonation is NOT in _net_info, before adding them.
        for (netID, component_id,
             pin_name) in self._net_info.itertuples(index=False):
            if ((component_id == comp1_id) and (pin_name == pin1_name)):
                self.logger.warning(
                    f'Component: {comp1_id} and pin: {pin1_name} are already in net_info with net_id {netID}'
                )
                return net_id
            if ((component_id == comp2_id) and (pin_name == pin2_name)):
                self.logger.warning(
                    f'Component: {comp2_id} and pin: {pin2_name} are already in net_info with net_id {netID}'
                )
                return net_id

        net_id = self._get_new_net_id()

        entry1 = [net_id, comp1_id, pin1_name]
        entry2 = [net_id, comp2_id, pin2_name]
        temp_df = pd.DataFrame([entry1, entry2], columns=self.column_names)

        self._net_info = self._net_info.append(temp_df, ignore_index=True)

        # print(self._net_info)
        return net_id

    def delete_net_id(self, net_id_to_remove: int):
        """
        Removes the two entries with net_id_to_remove.
        If id is in _net_info, the entry will be removed.

        Arguments:
            net_id_to_remove (int): The id to remove.
        """

        self._net_info.drop(
            self._net_info.index[self._net_info['net_id'] == net_id_to_remove],
            inplace=True)
        return

    def delete_all_pins_for_component(self, component_id_to_remove: int) -> set:
        """
        Delete all the pins for a given component id.

        Args:
            component_id_to_remove (int): Component ID to remove

        Returns:
            set: All deleted ids
        """
        all_net_id_deleted = set()

        for (netID, component_id,
             pin_name) in self._net_info.itertuples(index=False):
            if (component_id == component_id_to_remove):
                all_net_id_deleted.add(netID)
                self.delete_net_id(netID)

        return all_net_id_deleted

    def get_components_and_pins_for_netid(
            self, net_id_search: int) -> pd.core.frame.DataFrame:
        """Search with a net_id to get component id and pin name.

        Arguments:
            net_id_search (int): Unique net id which connects two pins within a design.

        Returns:
            pandas.DataFrame: Two rows of the net_info which have the same net_id_search.
        """
        df_subset_based_on_net_id = self._net_info[(
            self._net_info['net_id'] == net_id_search)]
        return df_subset_based_on_net_id
