import os
from pathlib import Path
import sys
from typing import Type, Optional, List

import pytest
from crytic_compile import CryticCompile, save_to_zip
from crytic_compile.utils.zip import load_from_zip

from solc_select import solc_select

from slither import Slither
from slither.detectors.abstract_detector import AbstractDetector
from slither.detectors import all_detectors


class Test:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        detector: Type[AbstractDetector],
        test_file: str,
        solc_ver: str,
        additional_files: Optional[List[str]] = None,
    ):
        """


        :param detector:
        :param test_file:
        :param solc_ver:
        :param additional_files: If the test changes additional files, list them here to allow the
        test to update the source mapping
        """
        self.detector = detector
        self.test_file = test_file
        self.solc_ver = solc_ver
        if additional_files is None:
            self.additional_files = []
        else:
            self.additional_files = additional_files


def set_solc(test_item: Test):  # pylint: disable=too-many-lines
    # hacky hack hack to pick the solc version we want
    env = dict(os.environ)

    if not solc_select.artifact_path(test_item.solc_ver).exists():
        print("Installing solc version", test_item.solc_ver)
        solc_select.install_artifacts([test_item.solc_ver])
    env["SOLC_VERSION"] = test_item.solc_ver
    os.environ.clear()
    os.environ.update(env)


def id_test(test_item: Test):
    return f"{test_item.detector.__name__}-{test_item.solc_ver}-{test_item.test_file}"


ALL_TESTS = [
    Test(
        all_detectors.UninitializedFunctionPtrsConstructor,
        "uninitialized_function_ptr_constructor.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UninitializedFunctionPtrsConstructor,
        "uninitialized_function_ptr_constructor.sol",
        "0.5.8",
    ),
    Test(
        all_detectors.UninitializedFunctionPtrsConstructor,
        "uninitialized_function_ptr_constructor.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ReentrancyBenign,
        "reentrancy-benign.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ReentrancyBenign,
        "reentrancy-benign.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ReentrancyBenign,
        "reentrancy-benign.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ReentrancyBenign,
        "reentrancy-benign.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "reentrancy-write.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "reentrancy-write.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "reentrancy-write.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "reentrancy-write.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "DAO.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "comment.sol",
        "0.8.2",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "no-reentrancy-staticcall.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "no-reentrancy-staticcall.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ReentrancyReadBeforeWritten,
        "no-reentrancy-staticcall.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.BooleanEquality,
        "boolean-constant-equality.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.BooleanEquality,
        "boolean-constant-equality.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.BooleanEquality,
        "boolean-constant-equality.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.BooleanEquality,
        "boolean-constant-equality.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.BooleanConstantMisuse,
        "boolean-constant-misuse.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.BooleanConstantMisuse,
        "boolean-constant-misuse.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.BooleanConstantMisuse,
        "boolean-constant-misuse.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.BooleanConstantMisuse,
        "boolean-constant-misuse.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UncheckedLowLevel,
        "unchecked_lowlevel.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UncheckedLowLevel,
        "unchecked_lowlevel.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UncheckedLowLevel,
        "unchecked_lowlevel.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UncheckedLowLevel,
        "unchecked_lowlevel.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnindexedERC20EventParameters,
        "erc20_indexed.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnindexedERC20EventParameters,
        "erc20_indexed.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnindexedERC20EventParameters,
        "erc20_indexed.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnindexedERC20EventParameters,
        "erc20_indexed.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.IncorrectERC20InterfaceDetection,
        "incorrect_erc20_interface.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.IncorrectERC20InterfaceDetection,
        "incorrect_erc20_interface.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.IncorrectERC20InterfaceDetection,
        "incorrect_erc20_interface.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.IncorrectERC20InterfaceDetection,
        "incorrect_erc20_interface.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.IncorrectERC721InterfaceDetection,
        "incorrect_erc721_interface.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.IncorrectERC721InterfaceDetection,
        "incorrect_erc721_interface.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.IncorrectERC721InterfaceDetection,
        "incorrect_erc721_interface.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.IncorrectERC721InterfaceDetection,
        "incorrect_erc721_interface.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UninitializedStateVarsDetection,
        "uninitialized.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UninitializedStateVarsDetection,
        "uninitialized.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UninitializedStateVarsDetection,
        "uninitialized.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UninitializedStateVarsDetection,
        "uninitialized.sol",
        "0.7.6",
    ),
    Test(all_detectors.Backdoor, "backdoor.sol", "0.4.25"),
    Test(all_detectors.Backdoor, "backdoor.sol", "0.5.16"),
    Test(all_detectors.Backdoor, "backdoor.sol", "0.6.11"),
    Test(all_detectors.Backdoor, "backdoor.sol", "0.7.6"),
    Test(all_detectors.Suicidal, "suicidal.sol", "0.4.25"),
    Test(all_detectors.Suicidal, "suicidal.sol", "0.5.16"),
    Test(all_detectors.Suicidal, "suicidal.sol", "0.6.11"),
    Test(all_detectors.Suicidal, "suicidal.sol", "0.7.6"),
    Test(
        all_detectors.ConstantPragma,
        "pragma.0.4.25.sol",
        "0.4.25",
        ["pragma.0.4.24.sol"],
    ),
    Test(
        all_detectors.ConstantPragma,
        "pragma.0.5.16.sol",
        "0.5.16",
        ["pragma.0.5.15.sol"],
    ),
    Test(
        all_detectors.ConstantPragma,
        "pragma.0.6.11.sol",
        "0.6.11",
        ["pragma.0.6.10.sol"],
    ),
    Test(
        all_detectors.ConstantPragma,
        "pragma.0.7.6.sol",
        "0.7.6",
        ["pragma.0.7.5.sol"],
    ),
    Test(all_detectors.IncorrectSolc, "static.sol", "0.4.25"),
    Test(all_detectors.IncorrectSolc, "static.sol", "0.5.14"),
    Test(all_detectors.IncorrectSolc, "static.sol", "0.5.16"),
    Test(all_detectors.IncorrectSolc, "dynamic_1.sol", "0.5.16"),
    Test(all_detectors.IncorrectSolc, "dynamic_2.sol", "0.5.16"),
    Test(all_detectors.IncorrectSolc, "static.sol", "0.6.10"),
    Test(all_detectors.IncorrectSolc, "static.sol", "0.6.11"),
    Test(all_detectors.IncorrectSolc, "dynamic_1.sol", "0.6.11"),
    Test(all_detectors.IncorrectSolc, "dynamic_2.sol", "0.6.11"),
    Test(all_detectors.IncorrectSolc, "static.sol", "0.7.4"),
    Test(all_detectors.IncorrectSolc, "static.sol", "0.7.6"),
    Test(all_detectors.IncorrectSolc, "dynamic_1.sol", "0.7.6"),
    Test(all_detectors.IncorrectSolc, "dynamic_2.sol", "0.7.6"),
    Test(
        all_detectors.ReentrancyEth,
        "reentrancy.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ReentrancyEth,
        "reentrancy_indirect.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ReentrancyEth,
        "reentrancy.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ReentrancyEth,
        "reentrancy_indirect.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ReentrancyEth,
        "reentrancy.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ReentrancyEth,
        "reentrancy_indirect.sol",
        "0.6.11",
    ),
    Test(all_detectors.ReentrancyEth, "reentrancy.sol", "0.7.6"),
    Test(
        all_detectors.ReentrancyEth,
        "reentrancy_indirect.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ReentrancyEth,
        "DAO.sol",
        "0.4.25",
    ),
    # Test the nonReentrant filtering
    Test(all_detectors.ReentrancyEth, "reentrancy_with_non_reentrant.sol", "0.8.10"),
    # Test parse_ignore_comments
    Test(all_detectors.ReentrancyEth, "reentrancy_filtered_comments.sol", "0.8.10"),
    Test(
        all_detectors.UninitializedStorageVars,
        "uninitialized_storage_pointer.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UninitializedStorageVars,
        "uninitialized_storage_pointer.sol",
        "0.8.19",
    ),
    Test(all_detectors.TxOrigin, "tx_origin.sol", "0.4.25"),
    Test(all_detectors.TxOrigin, "tx_origin.sol", "0.5.16"),
    Test(all_detectors.TxOrigin, "tx_origin.sol", "0.6.11"),
    Test(all_detectors.TxOrigin, "tx_origin.sol", "0.7.6"),
    Test(
        all_detectors.UnusedStateVars,
        "unused_state.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnusedStateVars,
        "unused_state.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnusedStateVars,
        "unused_state.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnusedStateVars,
        "unused_state.sol",
        "0.7.6",
    ),
    Test(all_detectors.LockedEther, "locked_ether.sol", "0.4.25"),
    Test(all_detectors.LockedEther, "locked_ether.sol", "0.5.16"),
    Test(all_detectors.LockedEther, "locked_ether.sol", "0.6.11"),
    Test(all_detectors.LockedEther, "locked_ether.sol", "0.7.6"),
    Test(
        all_detectors.ArbitrarySendEth,
        "arbitrary_send_eth.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ArbitrarySendEth,
        "arbitrary_send_eth.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ArbitrarySendEth,
        "arbitrary_send_eth.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ArbitrarySendEth,
        "arbitrary_send_eth.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_contract.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_library.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_contract.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_library.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_contract.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_library.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_contract.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.Assembly,
        "inline_assembly_library.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.LowLevelCalls,
        "low_level_calls.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.LowLevelCalls,
        "low_level_calls.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.LowLevelCalls,
        "low_level_calls.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.LowLevelCalls,
        "low_level_calls.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.CouldBeConstant,
        "const_state_variables.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.CouldBeConstant,
        "const_state_variables.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.CouldBeConstant,
        "const_state_variables.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.CouldBeConstant,
        "const_state_variables.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.CouldBeConstant,
        "const_state_variables.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.CouldBeConstant,
        "unused_yul.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.CouldBeImmutable,
        "immut_state_variables.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.CouldBeImmutable,
        "immut_state_variables.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.CouldBeImmutable,
        "immut_state_variables.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.CouldBeImmutable,
        "immut_state_variables.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.CouldBeImmutable,
        "immut_state_variables.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_2.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_3.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_2.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_3.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_2.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_3.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_2.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ExternalFunction,
        "external_function_3.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.NamingConvention,
        "naming_convention.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.NamingConvention,
        "naming_convention.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.NamingConvention,
        "naming_convention.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.NamingConvention,
        "naming_convention.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.NamingConvention,
        "no_warning_for_public_constants.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.NamingConvention,
        "no_warning_for_public_constants.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.NamingConvention,
        "no_warning_for_public_constants.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.NamingConvention,
        "no_warning_for_public_constants.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ControlledDelegateCall,
        "controlled_delegatecall.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ControlledDelegateCall,
        "controlled_delegatecall.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ControlledDelegateCall,
        "controlled_delegatecall.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ControlledDelegateCall,
        "controlled_delegatecall.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UninitializedLocalVars,
        "uninitialized_local_variable.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UninitializedLocalVars,
        "uninitialized_local_variable.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UninitializedLocalVars,
        "uninitialized_local_variable.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UninitializedLocalVars,
        "uninitialized_local_variable.sol",
        "0.7.6",
    ),
    Test(all_detectors.ConstantFunctionsAsm, "constant.sol", "0.4.25"),
    Test(
        all_detectors.ConstantFunctionsState,
        "constant.sol",
        "0.4.25",
    ),
    Test(all_detectors.ConstantFunctionsAsm, "constant.sol", "0.5.16"),
    Test(
        all_detectors.ConstantFunctionsState,
        "constant.sol",
        "0.5.16",
    ),
    Test(all_detectors.ConstantFunctionsAsm, "constant.sol", "0.6.11"),
    Test(
        all_detectors.ConstantFunctionsState,
        "constant.sol",
        "0.6.11",
    ),
    Test(all_detectors.ConstantFunctionsAsm, "constant.sol", "0.7.6"),
    Test(all_detectors.ConstantFunctionsState, "constant.sol", "0.7.6"),
    Test(
        all_detectors.UnusedReturnValues,
        "unused_return.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnusedReturnValues,
        "unused_return.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnusedReturnValues,
        "unused_return.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnusedReturnValues,
        "unused_return.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UncheckedTransfer,
        "unused_return_transfers.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ShadowingAbstractDetection,
        "shadowing_abstract.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ShadowingAbstractDetection,
        "shadowing_abstract.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ShadowingAbstractDetection,
        "shadowing_state_variable.sol",
        "0.7.5",
    ),
    Test(
        all_detectors.ShadowingAbstractDetection,
        "public_gap_variable.sol",
        "0.7.5",
    ),
    Test(
        all_detectors.StateShadowing,
        "shadowing_state_variable.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.StateShadowing,
        "shadowing_state_variable.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.StateShadowing,
        "shadowing_state_variable.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.StateShadowing,
        "shadowing_state_variable.sol",
        "0.7.5",
    ),
    Test(
        all_detectors.StateShadowing,
        "public_gap_variable.sol",
        "0.7.5",
    ),
    Test(
        all_detectors.StateShadowing,
        "shadowing_state_variable.sol",
        "0.7.6",
    ),
    Test(all_detectors.Timestamp, "timestamp.sol", "0.4.25"),
    Test(all_detectors.Timestamp, "timestamp.sol", "0.5.16"),
    Test(all_detectors.Timestamp, "timestamp.sol", "0.6.11"),
    Test(all_detectors.Timestamp, "timestamp.sol", "0.7.6"),
    Test(
        all_detectors.MultipleCallsInLoop,
        "multiple_calls_in_loop.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MultipleCallsInLoop,
        "multiple_calls_in_loop.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.MultipleCallsInLoop,
        "multiple_calls_in_loop.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.MultipleCallsInLoop,
        "multiple_calls_in_loop.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.BuiltinSymbolShadowing,
        "shadowing_builtin_symbols.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.BuiltinSymbolShadowing,
        "shadowing_builtin_symbols.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.LocalShadowing,
        "shadowing_local_variable.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.LocalShadowing,
        "shadowing_local_variable.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.LocalShadowing,
        "shadowing_local_variable.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.LocalShadowing,
        "shadowing_local_variable.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.RightToLeftOverride,
        "right_to_left_override.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.RightToLeftOverride,
        "right_to_left_override.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.RightToLeftOverride,
        "right_to_left_override.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.RightToLeftOverride,
        "unicode_direction_override.sol",
        "0.8.0",
    ),
    Test(all_detectors.VoidConstructor, "void-cst.sol", "0.4.25"),
    Test(all_detectors.VoidConstructor, "void-cst.sol", "0.5.16"),
    Test(all_detectors.VoidConstructor, "void-cst.sol", "0.6.11"),
    Test(all_detectors.VoidConstructor, "void-cst.sol", "0.7.6"),
    Test(
        all_detectors.UncheckedSend,
        "unchecked_send.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UncheckedSend,
        "unchecked_send.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UncheckedSend,
        "unchecked_send.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UncheckedSend,
        "unchecked_send.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ReentrancyEvent,
        "reentrancy-events.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ReentrancyEvent,
        "reentrancy-events.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ReentrancyEvent,
        "reentrancy-events.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.IncorrectStrictEquality,
        "incorrect_equality.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.IncorrectStrictEquality,
        "incorrect_equality.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.IncorrectStrictEquality,
        "incorrect_equality.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.IncorrectStrictEquality,
        "incorrect_equality.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.TooManyDigits,
        "too_many_digits.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.TooManyDigits,
        "too_many_digits.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.TooManyDigits,
        "too_many_digits.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.TooManyDigits,
        "too_many_digits.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Buggy.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Fixed.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "whitelisted.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Reinitializer.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "AnyInitializer.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Buggy.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Fixed.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "whitelisted.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Reinitializer.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "AnyInitializer.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Buggy.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Fixed.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "whitelisted.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Reinitializer.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "AnyInitializer.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Buggy.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Fixed.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Reinitializer.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "AnyInitializer.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "whitelisted.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Buggy.sol",
        "0.8.15",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Fixed.sol",
        "0.8.15",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "whitelisted.sol",
        "0.8.15",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "Reinitializer.sol",
        "0.8.15",
    ),
    Test(
        all_detectors.UnprotectedUpgradeable,
        "AnyInitializer.sol",
        "0.8.15",
    ),
    Test(
        all_detectors.ABIEncoderV2Array,
        "storage_ABIEncoderV2_array.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ABIEncoderV2Array,
        "storage_ABIEncoderV2_array.sol",
        "0.5.10",
    ),
    Test(
        all_detectors.ABIEncoderV2Array,
        "storage_ABIEncoderV2_array.sol",
        "0.5.9",
    ),
    Test(
        all_detectors.ArrayByReference,
        "array_by_reference.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ArrayByReference,
        "array_by_reference.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ArrayByReference,
        "array_by_reference.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ArrayByReference,
        "array_by_reference.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.AssertStateChange,
        "assert_state_change.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.AssertStateChange,
        "assert_state_change.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.AssertStateChange,
        "assert_state_change.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.AssertStateChange,
        "assert_state_change.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ArrayLengthAssignment,
        "array_length_assignment.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ArrayLengthAssignment,
        "array_length_assignment.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.CostlyOperationsInLoop,
        "multiple_costly_operations_in_loop.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.CostlyOperationsInLoop,
        "multiple_costly_operations_in_loop.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.CostlyOperationsInLoop,
        "multiple_costly_operations_in_loop.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.CostlyOperationsInLoop,
        "multiple_costly_operations_in_loop.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.FunctionInitializedState,
        "function_init_state_variables.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.FunctionInitializedState,
        "function_init_state_variables.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.FunctionInitializedState,
        "function_init_state_variables.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.FunctionInitializedState,
        "function_init_state_variables.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.MappingDeletionDetection,
        "MappingDeletion.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MappingDeletionDetection,
        "MappingDeletion.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.MappingDeletionDetection,
        "MappingDeletion.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.MappingDeletionDetection,
        "MappingDeletion.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.PublicMappingNested,
        "public_mappings_nested.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.RedundantStatements,
        "redundant_statements.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.RedundantStatements,
        "redundant_statements.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.RedundantStatements,
        "redundant_statements.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.RedundantStatements,
        "redundant_statements.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ReusedBaseConstructor,
        "reused_base_constructor.sol",
        "0.4.21",
    ),
    Test(
        all_detectors.ReusedBaseConstructor,
        "reused_base_constructor.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.StorageSignedIntegerArray,
        "storage_signed_integer_array.sol",
        "0.5.10",
    ),
    Test(
        all_detectors.StorageSignedIntegerArray,
        "storage_signed_integer_array.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnimplementedFunctionDetection,
        "unimplemented.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.UnimplementedFunctionDetection,
        "unimplemented.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnimplementedFunctionDetection,
        "unimplemented.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnimplementedFunctionDetection,
        "unimplemented.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.UnimplementedFunctionDetection,
        "unimplemented_interfaces.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.UnimplementedFunctionDetection,
        "unimplemented_interfaces.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.UnimplementedFunctionDetection,
        "unimplemented_interfaces.sol",
        "0.7.6",
    ),
    Test(all_detectors.BadPRNG, "bad_prng.sol", "0.4.25"),
    Test(all_detectors.BadPRNG, "bad_prng.sol", "0.5.16"),
    Test(all_detectors.BadPRNG, "bad_prng.sol", "0.6.11"),
    Test(all_detectors.BadPRNG, "bad_prng.sol", "0.7.6"),
    Test(
        all_detectors.MissingEventsAccessControl,
        "missing_events_access_control.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MissingEventsAccessControl,
        "missing_events_access_control.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.MissingEventsAccessControl,
        "missing_events_access_control.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.MissingEventsAccessControl,
        "missing_events_access_control.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.MissingEventsArithmetic,
        "missing_events_arithmetic.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MissingEventsArithmetic,
        "missing_events_arithmetic.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.MissingEventsArithmetic,
        "missing_events_arithmetic.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.MissingEventsArithmetic,
        "missing_events_arithmetic.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ModifierDefaultDetection,
        "modifier_default.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ModifierDefaultDetection,
        "modifier_default.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ModifierDefaultDetection,
        "modifier_default.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ModifierDefaultDetection,
        "modifier_default.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.IncorrectUnaryExpressionDetection,
        "invalid_unary_expression.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MissingZeroAddressValidation,
        "missing_zero_address_validation.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MissingZeroAddressValidation,
        "missing_zero_address_validation.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.MissingZeroAddressValidation,
        "missing_zero_address_validation.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.MissingZeroAddressValidation,
        "missing_zero_address_validation.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.PredeclarationUsageLocal,
        "predeclaration_usage_local.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.DeadCode,
        "dead-code.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.WriteAfterWrite,
        "write-after-write.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.ShiftParameterMixup,
        "shift_parameter_mixup.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ShiftParameterMixup,
        "shift_parameter_mixup.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ShiftParameterMixup,
        "shift_parameter_mixup.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ShiftParameterMixup,
        "shift_parameter_mixup.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.MissingInheritance,
        "unimplemented_interface.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MissingInheritance,
        "unimplemented_interface.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.MissingInheritance,
        "unimplemented_interface.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.MissingInheritance,
        "unimplemented_interface.sol",
        "0.7.6",
    ),
    # Does not work on the CI. Most likely because of solc 0.4.2?
    # Test(
    #     all_detectors.EnumConversion,
    #     "enum_conversion.sol",
    #     "0.4.2",
    # ),
    Test(
        all_detectors.MultipleConstructorSchemes,
        "multiple_constructor_schemes.sol",
        "0.4.22",
    ),
    Test(
        all_detectors.DeprecatedStandards,
        "deprecated_calls.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.DivideBeforeMultiply,
        "divide_before_multiply.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.DivideBeforeMultiply,
        "divide_before_multiply.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.DivideBeforeMultiply,
        "divide_before_multiply.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.DivideBeforeMultiply,
        "divide_before_multiply.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.TypeBasedTautology,
        "type_based_tautology.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.TypeBasedTautology,
        "type_based_tautology.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.TypeBasedTautology,
        "type_based_tautology.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.TypeBasedTautology,
        "type_based_tautology.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.MsgValueInLoop,
        "msg_value_loop.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.MsgValueInLoop,
        "msg_value_loop.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.MsgValueInLoop,
        "msg_value_loop.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.MsgValueInLoop,
        "msg_value_loop.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.MsgValueInLoop,
        "msg_value_loop.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.DelegatecallInLoop,
        "delegatecall_loop.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.DelegatecallInLoop,
        "delegatecall_loop.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.DelegatecallInLoop,
        "delegatecall_loop.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.DelegatecallInLoop,
        "delegatecall_loop.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.DelegatecallInLoop,
        "delegatecall_loop.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.ProtectedVariables,
        "comment.sol",
        "0.8.2",
    ),
    Test(
        all_detectors.ArbitrarySendErc20NoPermit,
        "arbitrary_send_erc20.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ArbitrarySendErc20NoPermit,
        "arbitrary_send_erc20.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ArbitrarySendErc20NoPermit,
        "arbitrary_send_erc20.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ArbitrarySendErc20NoPermit,
        "arbitrary_send_erc20.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ArbitrarySendErc20NoPermit,
        "arbitrary_send_erc20.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.ArbitrarySendErc20NoPermit,
        "arbitrary_send_erc20_inheritance.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.ArbitrarySendErc20Permit,
        "arbitrary_send_erc20_permit.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.ArbitrarySendErc20Permit,
        "arbitrary_send_erc20_permit.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.ArbitrarySendErc20Permit,
        "arbitrary_send_erc20_permit.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.ArbitrarySendErc20Permit,
        "arbitrary_send_erc20_permit.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.ArbitrarySendErc20Permit,
        "arbitrary_send_erc20_permit.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_collision.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_collision.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_collision.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_collision.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_collision.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_wrong_return_type.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_wrong_return_type.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_wrong_return_type.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_wrong_return_type.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_wrong_return_type.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_state_var_collision.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_state_var_collision.sol",
        "0.5.16",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_state_var_collision.sol",
        "0.6.11",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_state_var_collision.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.DomainSeparatorCollision,
        "permit_domain_state_var_collision.sol",
        "0.8.0",
    ),
    Test(
        all_detectors.VarReadUsingThis,
        "var_read_using_this.sol",
        "0.4.25",
    ),
    Test(
        all_detectors.VarReadUsingThis,
        "var_read_using_this.sol",
        "0.5.16",
    ),
    Test(all_detectors.VarReadUsingThis, "var_read_using_this.sol", "0.6.11"),
    Test(
        all_detectors.VarReadUsingThis,
        "var_read_using_this.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.VarReadUsingThis,
        "var_read_using_this.sol",
        "0.8.15",
    ),
    Test(
        all_detectors.CyclomaticComplexity,
        "HighCyclomaticComplexity.sol",
        "0.8.16",
    ),
    Test(
        all_detectors.CyclomaticComplexity,
        "LowCyclomaticComplexity.sol",
        "0.8.16",
    ),
    Test(
        all_detectors.CacheArrayLength,
        "CacheArrayLength.sol",
        "0.8.17",
    ),
    Test(
        all_detectors.IncorrectUsingFor,
        "IncorrectUsingForTopLevel.sol",
        "0.8.17",
    ),
    Test(
        all_detectors.EncodePackedCollision,
        "encode_packed_collision.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.IncorrectReturn,
        "incorrect_return.sol",
        "0.8.10",
    ),
    Test(
        all_detectors.ReturnInsteadOfLeave,
        "incorrect_return.sol",
        "0.8.10",
    ),
    Test(
        all_detectors.IncorrectOperatorExponentiation,
        "incorrect_exp.sol",
        "0.7.6",
    ),
    Test(
        all_detectors.TautologicalCompare,
        "compare.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.ReturnBomb,
        "return_bomb.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.OutOfOrderRetryable,
        "out_of_order_retryable.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.GelatoUnprotectedRandomness,
        "gelato_unprotected_randomness.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.ChronicleUncheckedPrice,
        "chronicle_unchecked_price.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.PythUncheckedConfidence,
        "pyth_unchecked_confidence.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.PythUncheckedPublishTime,
        "pyth_unchecked_publishtime.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.ChainlinkFeedRegistry,
        "chainlink_feed_registry.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.PythDeprecatedFunctions,
        "pyth_deprecated_functions.sol",
        "0.8.20",
    ),
    Test(
        all_detectors.OptimismDeprecation,
        "optimism_deprecation.sol",
        "0.8.20",
    ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "ConstantContractLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "ConstantContractLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "ConstantTopLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "ConstantTopLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "ContractUsedInContractTest1.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "ContractUsedInContractTest2.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "ContractUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomErrorTopLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomEventContractLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomEventContractLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeContractLevelUsedInContractTest1.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeContractLevelUsedInContractTest2.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeContractLevelUsedInContractTest3.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeContractLevelUsedInContractTest4.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeContractLevelUsedTopLevelTest1.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeContractLevelUsedTopLevelTest2.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeTopLevelUsedInContractTest1.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeTopLevelUsedInContractTest2.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeTopLevelUsedInContractTest3.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeTopLevelUsedInContractTest4.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeTopLevelUsedTopLevelTest1.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "CustomTypeTopLevelUsedTopLevelTest2.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "EnumContractLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "EnumContractLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "EnumTopLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "EnumTopLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "FunctionContractLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "FunctionContractLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "FunctionTopLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "FunctionTopLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "LibraryUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "LibraryUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "StructContractLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "StructContractLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "StructTopLevelUsedInContractTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "StructTopLevelUsedTopLevelTest.sol",
    #     "0.8.16",
    # ),
    # Test(
    #     all_detectors.UnusedImport,
    #     "C.sol",
    #     "0.8.16",
    # ),
]

GENERIC_PATH = "/GENERIC_PATH"

TEST_DATA_DIR = Path(__file__).resolve().parent / "test_data"

# pylint: disable=too-many-locals
@pytest.mark.parametrize("test_item", ALL_TESTS, ids=id_test)
def test_detector(test_item: Test, snapshot):
    test_dir_path = Path(
        TEST_DATA_DIR,
        test_item.detector.ARGUMENT,
        test_item.solc_ver,
    ).as_posix()
    test_file_path = Path(test_dir_path, test_item.test_file).as_posix()

    zip_artifact_path = Path(f"{test_file_path}-{test_item.solc_ver}.zip").as_posix()
    crytic_compile = load_from_zip(zip_artifact_path)[0]

    sl = Slither(crytic_compile)
    sl.register_detector(test_item.detector)
    results = sl.run_detectors()

    actual_output = ""
    for detector_result in results:
        for result in detector_result:
            actual_output += result["description"]
            actual_output += "\n"
    assert snapshot() == actual_output


def _generate_compile(test_item: Test, skip_existing=False):
    test_dir_path = Path(
        TEST_DATA_DIR,
        test_item.detector.ARGUMENT,
        test_item.solc_ver,
    ).as_posix()
    test_file_path = Path(test_dir_path, test_item.test_file).as_posix()
    zip_artifact_path = Path(f"{test_file_path}-{test_item.solc_ver}.zip").as_posix()

    if skip_existing:
        if os.path.isfile(zip_artifact_path):
            return

    set_solc(test_item)
    crytic_compile = CryticCompile(test_file_path)
    save_to_zip([crytic_compile], zip_artifact_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "To generate the zip artifacts run\n\tpython tests/e2e/tests/test_detectors.py --compile"
        )
    elif sys.argv[1] == "--compile":
        for next_test in ALL_TESTS:
            _generate_compile(next_test, skip_existing=True)
