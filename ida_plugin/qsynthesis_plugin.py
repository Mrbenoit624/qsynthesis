#!/usr/bin/env python3

from qsynthesis.plugin.dependencies import ida_idaapi, ida_kernwin, QTRACEIDA_ENABLED, TRITON_ENABLED
import qsynthesis


class QSynthesisPlugin(ida_idaapi.plugin_t):
    flags = ida_idaapi.PLUGIN_UNL
    comment = "QSynthesis IDA plugin"
    help = "Plugin to perform program synthesis of symbolic expressions"
    wanted_name = "QSynthesis"
    wanted_hotkey = "Alt-S"

    def init(self):
        addon_info = ida_kernwin.addon_info_t()
        addon_info.id = "com.quarkslab.qtraceida.qsynthesis.plugin"
        addon_info.name = self.wanted_name
        addon_info.producer = "Quarkslab"
        addon_info.version = qsynthesis.__version__
        addon_info.url = "https://gitlab.qb/synthesis/qsynthesis"
        addon_info.freeform = "Copyright (c) 2020 - All Rights Reserved"
        ida_kernwin.register_addon(addon_info)
        return ida_idaapi.PLUGIN_OK if TRITON_ENABLED else ida_idaapi.PLUGIN_SKIP

    def run(self, arg):
        print("Running QSynthesis")
        if QTRACEIDA_ENABLED:
            import qtraceida
            qtr = qtraceida.get_qtrace()
        else:
            qtr = None
        from qsynthesis.plugin.view import SynthesizerView
        self.view = SynthesizerView(qtr)
        # self.view.init()
        self.view.Show()  # Show will call OnCreate that will call init

    def term(self):
        pass


def PLUGIN_ENTRY():
    return QSynthesisPlugin()


def main():
    # Standalone IDA-less mode. This way of launching QSynthesis
    # is mostly here for testing more rapidely without IDA
    import sys
    from PyQt5.QtWidgets import QApplication
    from qsynthesis.plugin.view import SynthesizerView
    app = QApplication(sys.argv)
    widget = SynthesizerView("")
    widget.init()
    widget.show()
    app.exec_()


if __name__ == "__main__":
    main()
