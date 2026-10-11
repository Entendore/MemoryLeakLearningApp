#!/usr/bin/env python3
"""
Memory Error Learning Application
==================================
An interactive application for learning about memory-related errors
such as segmentation faults, bus errors, stack overflows, and more.
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QStackedWidget, QLabel, QTextBrowser, QPushButton,
    QGroupBox, QRadioButton, QButtonGroup, QTabWidget, QSplitter,
    QFrame, QSizePolicy, QScrollArea, QProgressBar, QMessageBox,
    QGridLayout, QSpacerItem, QScrollArea, QToolButton, QComboBox
)
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QRectF
from PySide6.QtGui import (
    QPainter, QColor, QFont, QPen, QBrush, QPainterPath,
    QLinearGradient, QFontMetrics, QTextCursor, QIcon
)

# ─── Dark Theme Stylesheet ───────────────────────────────────────────────────

DARK_STYLESHEET = """
QMainWindow {
    background-color: #1a1b2e;
}
QWidget {
    background-color: #1a1b2e;
    color: #e2e8f0;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}
QListWidget {
    background-color: #16172b;
    border: none;
    border-right: 2px solid #2d2f52;
    outline: none;
    font-size: 13px;
    padding: 8px 4px;
}
QListWidget::item {
    padding: 12px 16px;
    border-radius: 8px;
    margin: 2px 4px;
    color: #a0a4c8;
}
QListWidget::item:selected {
    background-color: #7c3aed;
    color: #ffffff;
    font-weight: bold;
}
QListWidget::item:hover:!selected {
    background-color: #2d2f52;
    color: #e2e8f0;
}
QTabWidget::pane {
    border: 1px solid #2d2f52;
    border-radius: 8px;
    background-color: #1e1f36;
    padding: 4px;
}
QTabBar::tab {
    background-color: #16172b;
    color: #a0a4c8;
    padding: 10px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
    font-size: 13px;
}
QTabBar::tab:selected {
    background-color: #1e1f36;
    color: #7c3aed;
    font-weight: bold;
    border-bottom: 2px solid #7c3aed;
}
QTabBar::tab:hover:!selected {
    background-color: #2d2f52;
    color: #e2e8f0;
}
QTextBrowser {
    background-color: #12132a;
    border: 1px solid #2d2f52;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    color: #e2e8f0;
}
QGroupBox {
    background-color: #1e1f36;
    border: 1px solid #2d2f52;
    border-radius: 10px;
    margin-top: 16px;
    padding: 20px 16px 16px 16px;
    font-weight: bold;
    font-size: 14px;
    color: #7c3aed;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 4px 12px;
    background-color: #7c3aed;
    color: white;
    border-radius: 4px;
}
QPushButton {
    background-color: #7c3aed;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #6d28d9;
}
QPushButton:pressed {
    background-color: #5b21b6;
}
QPushButton:disabled {
    background-color: #3b3b5c;
    color: #666688;
}
QPushButton#secondary {
    background-color: #2d2f52;
    color: #a0a4c8;
    border: 1px solid #3d3f72;
}
QPushButton#secondary:hover {
    background-color: #3d3f72;
    color: #e2e8f0;
}
QPushButton#danger {
    background-color: #dc2626;
}
QPushButton#danger:hover {
    background-color: #b91c1c;
}
QPushButton#success {
    background-color: #16a34a;
}
QPushButton#success:hover {
    background-color: #15803d;
}
QRadioButton {
    spacing: 8px;
    font-size: 14px;
    color: #e2e8f0;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #4a4d7a;
    background-color: #16172b;
}
QRadioButton::indicator:checked {
    border-color: #7c3aed;
    background-color: #7c3aed;
}
QProgressBar {
    border: 1px solid #2d2f52;
    border-radius: 8px;
    text-align: center;
    background-color: #16172b;
    color: #e2e8f0;
    font-weight: bold;
    height: 24px;
}
QProgressBar::chunk {
    background-color: #7c3aed;
    border-radius: 7px;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
QSplitter::handle {
    background-color: #2d2f52;
    width: 2px;
}
QLabel#title {
    font-size: 24px;
    font-weight: bold;
    color: #7c3aed;
}
QLabel#subtitle {
    font-size: 16px;
    color: #a0a4c8;
}
QLabel#signal_badge {
    background-color: #dc2626;
    color: white;
    border-radius: 4px;
    padding: 4px 10px;
    font-weight: bold;
    font-size: 12px;
}
"""


# ─── Error Content Data ──────────────────────────────────────────────────────

ERROR_DATA = {
    "overview": {
        "title": "Overview: Memory Errors",
        "icon": "🧠",
        "signal": None,
    },
    "segfault": {
        "title": "Segmentation Fault",
        "icon": "💥",
        "signal": "SIGSEGV (Signal 11)",
        "summary": "A segmentation fault occurs when a program tries to access a memory location that it is not allowed to access, or tries to access memory in a way that is not permitted.",
        "description": """
<h2>What is a Segmentation Fault?</h2>
<p>A <b>segmentation fault</b> (segfault) is one of the most common runtime errors in C/C++ programs.
It occurs when a program attempts to access a memory segment that it does not have permission to access,
or when it tries to perform an invalid memory operation.</p>

<h3>How Virtual Memory Works</h3>
<p>Modern operating systems use <b>virtual memory</b> with memory protection. Each process has its own
virtual address space divided into <b>segments</b>. The OS maintains a page table that maps virtual
addresses to physical addresses. When a program accesses memory:</p>
<ul>
<li>The CPU checks the page table</li>
<li>If the page is valid and accessible → access granted</li>
<li>If the page is invalid or access denied → <b>SIGSEGV</b> is raised</li>
</ul>

<h3>Key Concept: Segments</h3>
<p>Memory is divided into segments with different permissions:</p>
<ul>
<li><b>Text (Code)</b>: Read + Execute only</li>
<li><b>Data/BSS</b>: Read + Write (initialized/uninitialized globals)</li>
<li><b>Heap</b>: Read + Write (dynamically allocated)</li>
<li><b>Stack</b>: Read + Write (local variables, return addresses)</li>
<li><b>Kernel space</b>: No access from user space</li>
</ul>
""",
        "causes": [
            ("Dereferencing NULL pointer", "Accessing memory at address 0, which is never mapped"),
            ("Dereferencing uninitialized pointer", "The pointer contains a garbage address"),
            ("Accessing freed memory", "The memory has been returned to the OS/allocator"),
            ("Buffer overflow (write)", "Writing past the end of an allocated buffer"),
            ("Stack overflow", "Infinite recursion exhausting the stack"),
            ("Accessing out-of-scope memory", "Using a pointer to a local variable after function returns"),
        ],
        "code_examples": [
            {
                "title": "NULL Pointer Dereference",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdio.h&gt;</span>

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">*ptr</span> = <span style="color:#ef4444;">NULL</span>;
    
    <span style="color:#6b7280;">// 💥 Segfault: accessing address 0x0</span>
    <span style="color:#f59e0b;">*ptr</span> = <span style="color:#06b6d4;">42</span>;
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ The program tries to write to address 0, which is never mapped in any process.</p>""",
            },
            {
                "title": "Use After Free",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdlib.h&gt;</span>
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdio.h&gt;</span>

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">*data</span> = (<span style="color:#7c3aed;">int</span>*)<span style="color:#22c55e;">malloc</span>(<span style="color:#7c3aed;">sizeof</span>(<span style="color:#7c3aed;">int</span>));
    <span style="color:#f59e0b;">*data</span> = <span style="color:#06b6d4;">100</span>;
    
    <span style="color:#22c55e;">free</span>(<span style="color:#f59e0b;">data</span>);
    
    <span style="color:#6b7280;">// 💥 Segfault (or undefined behavior):</span>
    <span style="color:#6b7280;">// Accessing freed memory</span>
    <span style="color:#22c55e;">printf</span>(<span style="color:#06b6d4;">"%d\\n"</span>, <span style="color:#f59e0b;">*data</span>);
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ After free(), the memory may be unmapped or reused. Accessing it is undefined behavior.</p>""",
            },
            {
                "title": "Dangling Pointer (Out-of-Scope Access)",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdio.h&gt;</span>

<span style="color:#7c3aed;">int</span>* <span style="color:#22c55e;">create_dangling</span>() {
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">local</span> = <span style="color:#06b6d4;">42</span>;
    <span style="color:#6b7280;">// Returns address of local variable</span>
    <span style="color:#7c3aed;">return</span> &amp;<span style="color:#f59e0b;">local</span>;
    <span style="color:#6b7280;">// 'local' is destroyed when function returns</span>
}

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">*ptr</span> = <span style="color:#22c55e;">create_dangling</span>();
    
    <span style="color:#6b7280;">// 💥 Segfault: ptr points to destroyed stack frame</span>
    <span style="color:#22c55e;">printf</span>(<span style="color:#06b6d4;">"%d\\n"</span>, <span style="color:#f59e0b;">*ptr</span>);
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ The stack frame is deallocated when the function returns. The pointer is now dangling.</p>""",
            },
        ],
        "detection": """
<h3>Detection Tools</h3>
<ul>
<li><b>AddressSanitizer (ASan)</b>: Compile with <code>-fsanitize=address</code> — detects use-after-free, buffer overflows, etc.</li>
<li><b>Valgrind</b>: Runtime memory error detector — <code>valgrind --leak-check=full ./program</code></li>
<li><b>GDB</b>: Debug with <code>gdb ./program</code>, then <code>run</code> and <code>bt</code> for backtrace</li>
<li><b>Dr. Memory</b>: Cross-platform memory debugger</li>
</ul>

<h3>Fix Strategies</h3>
<ol>
<li>Always initialize pointers to <code>NULL</code></li>
<li>Check for <code>NULL</code> before dereferencing</li>
<li>Set pointers to <code>NULL</code> after <code>free()</code></li>
<li>Use <code>sizeof()</code> correctly with <code>malloc()</code></li>
<li>Avoid returning pointers to local variables</li>
<li>Use smart pointers in C++ (<code>std::unique_ptr</code>, <code>std::shared_ptr</code>)</li>
</ol>
""",
        "quiz": {
            "question": "What happens when you dereference a NULL pointer in C?",
            "options": [
                "It returns 0",
                "It causes undefined behavior, typically a segmentation fault",
                "The compiler catches it at compile time",
                "The OS allocates a new page at address 0"
            ],
            "correct": 1,
            "explanation": "Dereferencing NULL (address 0) is undefined behavior. On most modern OSes, address 0 is never mapped, so the CPU raises a page fault which the kernel converts to SIGSEGV."
        }
    },
    "bus_error": {
        "title": "Bus Error",
        "icon": "🚌",
        "signal": "SIGBUS (Signal 7/10)",
        "summary": "A bus error occurs when a program accesses memory that the CPU cannot physically address, or when it performs an unaligned memory access on architectures that require alignment.",
        "description": """
<h2>What is a Bus Error?</h2>
<p>A <b>bus error</b> is raised when the CPU cannot carry out a memory access request.
This typically happens for two reasons:</p>

<h3>1. Unaligned Memory Access</h3>
<p>Many CPU architectures (ARM, SPARC, older MIPS) require that multi-byte accesses
be <b>aligned</b> to their natural boundary:</p>
<ul>
<li><b>4-byte int</b> must be at an address divisible by 4</li>
<li><b>8-byte double</b> must be at an address divisible by 8</li>
</ul>
<p>x86/x64 is permissive — it handles unaligned accesses in hardware (with a performance penalty).
But ARM and other RISC architectures raise <b>SIGBUS</b>.</p>

<h3>2. Non-Existent Memory</h3>
<p>Accessing a memory address that the hardware cannot physically address
(not just unmapped — truly non-existent in the address space).</p>

<h3>Segfault vs Bus Error</h3>
<table style="width:100%; border-collapse:collapse;">
<tr style="background:#2d2f52;"><th style="padding:8px; text-align:left;">Aspect</th><th style="padding:8px;">SIGSEGV</th><th style="padding:8px;">SIGBUS</th></tr>
<tr><td style="padding:8px;">Cause</td><td style="padding:8px;">Invalid permissions / unmapped</td><td style="padding:8px;">Alignment / hardware issue</td></tr>
<tr style="background:#1a1b2e;"><td style="padding:8px;">Level</td><td style="padding:8px;">OS (page fault)</td><td style="padding:8px;">CPU (bus fault)</td></tr>
<tr><td style="padding:8px;">Frequency</td><td style="padding:8px;">Very common</td><td style="padding:8px;">Less common</td></tr>
<tr style="background:#1a1b2e;"><td style="padding:8px;">x86 behavior</td><td style="padding:8px;">Common</td><td style="padding:8px;">Rare (x86 handles alignment)</td></tr>
</table>
""",
        "causes": [
            ("Unaligned access on strict architectures", "Reading an int from an address not divisible by 4 on ARM/SPARC"),
            ("Accessing memory-mapped I/O incorrectly", "Reading from a write-only memory-mapped device register"),
            ("Non-existent physical address", "Accessing an address the hardware cannot reach"),
            ("Corrupted pointer with odd address", "Using a corrupted pointer that happens to be misaligned"),
        ],
        "code_examples": [
            {
                "title": "Unaligned Memory Access",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdio.h&gt;</span>
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdlib.h&gt;</span>
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;string.h&gt;</span>

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">char</span> <span style="color:#f59e0b;">buffer</span>[<span style="color:#06b6d4;">8</span>] = {<span style="color:#06b6d4;">1</span>,<span style="color:#06b6d4;">2</span>,<span style="color:#06b6d4;">3</span>,<span style="color:#06b6d4;">4</span>,<span style="color:#06b6d4;">5</span>,<span style="color:#06b6d4;">6</span>,<span style="color:#06b6d4;">7</span>,<span style="color:#06b6d4;">8</span>};
    
    <span style="color:#6b7280;">// 💥 Bus Error on ARM/SPARC:</span>
    <span style="color:#6b7280;">// Accessing int at odd address (buffer+1)</span>
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">*iptr</span> = (<span style="color:#7c3aed;">int</span>*)(<span style="color:#f59e0b;">buffer</span> + <span style="color:#06b6d4;">1</span>);
    <span style="color:#22c55e;">printf</span>(<span style="color:#06b6d4;">"%d\\n"</span>, <span style="color:#f59e0b;">*iptr</span>);
    
    <span style="color:#6b7280;">// ✅ Correct: use memcpy for unaligned access</span>
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">value</span>;
    <span style="color:#22c55e;">memcpy</span>(&amp;<span style="color:#f59e0b;">value</span>, <span style="color:#f59e0b;">buffer</span> + <span style="color:#06b6d4;">1</span>, <span style="color:#7c3aed;">sizeof</span>(<span style="color:#7c3aed;">int</span>));
    <span style="color:#22c55e;">printf</span>(<span style="color:#06b6d4;">"%d\\n"</span>, <span style="color:#f59e0b;">value</span>);
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ On ARM, casting buffer+1 to int* and dereferencing causes SIGBUS because the address is not 4-byte aligned.</p>""",
            },
        ],
        "detection": """
<h3>Detection Tools</h3>
<ul>
<li><b>AddressSanitizer</b>: Can detect some alignment issues with <code>-fsanitize=alignment</code></li>
<li><b>UBSan (Undefined Behavior Sanitizer)</b>: <code>-fsanitize=undefined</code> catches alignment violations</li>
<li><b>Valgrind</b>: Reports unaligned accesses with <code>--tool=memcheck</code></li>
<li><b>Compiler warnings</b>: <code>-Wcast-align</code> warns about potentially unaligned casts</li>
</ul>

<h3>Fix Strategies</h3>
<ol>
<li>Use <code>memcpy()</code> instead of pointer casting for potentially unaligned access</li>
<li>Use <code>__attribute__((packed))</code> carefully in structs</li>
<li>Compile with <code>-Wcast-align</code> to get warnings</li>
<li>Use <code>alignas()</code> (C11/C++11) to specify alignment</li>
<li>On ARM, use <code>-mno-unaligned-access</code> to catch issues during development</li>
</ol>
""",
        "quiz": {
            "question": "Why does a bus error due to unaligned access occur on ARM but typically not on x86?",
            "options": [
                "ARM has less memory than x86",
                "x86 hardware handles unaligned accesses transparently (with a performance penalty), while ARM raises a fault",
                "ARM doesn't have a memory management unit",
                "x86 programs never have alignment issues"
            ],
            "correct": 1,
            "explanation": "x86/x64 CPUs are designed to handle unaligned accesses in microcode — they work but are slower. ARM and other RISC architectures are designed for simplicity and require aligned accesses, raising SIGBUS for violations."
        }
    },
    "stack_overflow": {
        "title": "Stack Overflow",
        "icon": "📚",
        "signal": "SIGSEGV (Signal 11)",
        "summary": "A stack overflow occurs when the call stack pointer exceeds the stack's bounds, usually due to excessive recursion or very large stack allocations.",
        "description": """
<h2>What is a Stack Overflow?</h2>
<p>A <b>stack overflow</b> occurs when a program uses more stack memory than is allocated.
The stack is a fixed-size region of memory (typically 1-8 MB on Linux) used for:</p>
<ul>
<li>Local variables</li>
<li>Function call frames (return address, saved registers)</li>
<li>Function arguments</li>
</ul>

<h3>Stack Layout</h3>
<p>The stack grows downward (from high to low addresses). Each function call pushes
a new <b>stack frame</b>. When the stack pointer goes below the allocated region,
the OS raises <b>SIGSEGV</b> (because the memory is unmapped).</p>

<h3>Typical Stack Sizes</h3>
<ul>
<li>Linux: default 8 MB (<code>ulimit -s</code>)</li>
<li>Windows: default 1 MB</li>
<li>macOS: default 8 MB (main thread), 512 KB (secondary threads)</li>
</ul>
""",
        "causes": [
            ("Infinite/unbounded recursion", "No base case or base case never reached, causing infinite stack frames"),
            ("Very large stack allocations", "Declaring large arrays as local variables (e.g., int arr[10000000])"),
            ("Deeply nested function calls", "Function call chain too deep"),
            ("Alloca in a loop", "Using alloca() repeatedly which allocates on the stack"),
        ],
        "code_examples": [
            {
                "title": "Infinite Recursion",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdio.h&gt;</span>

<span style="color:#7c3aed;">void</span> <span style="color:#22c55e;">infinite_recursion</span>(<span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">n</span>) {
    <span style="color:#7c3aed;">char</span> <span style="color:#f59e0b;">big_array</span>[<span style="color:#06b6d4;">1024</span>];  <span style="color:#6b7280;">// Uses 1KB per call</span>
    
    <span style="color:#22c55e;">printf</span>(<span style="color:#06b6d4;">"Call depth: %d\\n"</span>, <span style="color:#f59e0b;">n</span>);
    
    <span style="color:#6b7280;">// 💥 No base case! Stack will grow until overflow</span>
    <span style="color:#22c55e;">infinite_recursion</span>(<span style="color:#f59e0b;">n</span> + <span style="color:#06b6d4;">1</span>);
}

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#22c55e;">infinite_recursion</span>(<span style="color:#06b6d4;">1</span>);
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ Each recursive call adds a new stack frame. Without a base case, the stack grows until it overflows.</p>""",
            },
            {
                "title": "Large Stack Allocation",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdio.h&gt;</span>

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#6b7280;">// 💥 Trying to allocate 100MB on stack</span>
    <span style="color:#6b7280;">// Default stack is only ~8MB</span>
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">huge_array</span>[<span style="color:#06b6d4;">25000000</span>];
    
    <span style="color:#f59e0b;">huge_array</span>[<span style="color:#06b6d4;">0</span>] = <span style="color:#06b6d4;">42</span>;  <span style="color:#6b7280;">// Stack overflow!</span>
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ Use malloc()/new for large allocations. Stack space is limited and fixed at program start.</p>""",
            },
        ],
        "detection": """
<h3>Detection</h3>
<ul>
<li><b>Stack overflow detection</b>: Compile with <code>-fstack-protector-all</code></li>
<li><b>GDB</b>: The backtrace will show very deep recursion</li>
<li><b>AddressSanitizer</b>: Detects stack buffer overflows</li>
<li><b>ThreadSanitizer</b>: Can detect stack data races</li>
<li><b>ulimit -s</b>: Check current stack size limit</li>
</ul>

<h3>Fix Strategies</h3>
<ol>
<li>Ensure all recursive functions have a proper base case</li>
<li>Convert deep recursion to iteration</li>
<li>Use <code>malloc()</code>/<code>new</code> for large allocations</li>
<li>Increase stack size: <code>ulimit -s unlimited</code> or <code>pthread_attr_setstacksize()</code></li>
<li>Use tail recursion (some compilers optimize this)</li>
</ol>
""",
        "quiz": {
            "question": "What is the default stack size on most Linux systems?",
            "options": [
                "64 KB",
                "1 MB",
                "8 MB",
                "Unlimited"
            ],
            "correct": 2,
            "explanation": "The default stack size on most Linux distributions is 8 MB, which can be checked with 'ulimit -s' and changed with 'ulimit -s <size>'."
        }
    },
    "buffer_overflow": {
        "title": "Buffer Overflow",
        "icon": "📦",
        "signal": "SIGSEGV / Undefined Behavior",
        "summary": "A buffer overflow occurs when data is written beyond the boundaries of a buffer, overwriting adjacent memory which can lead to crashes or security vulnerabilities.",
        "description": """
<h2>What is a Buffer Overflow?</h2>
<p>A <b>buffer overflow</b> occurs when a program writes data past the end (or before the beginning)
of an allocated buffer. This is one of the most dangerous memory errors because:</p>
<ul>
<li>It can corrupt adjacent data structures</li>
<li>It can overwrite return addresses on the stack</li>
<li>It is a major security vulnerability (exploited by malware)</li>
</ul>

<h3>Stack Buffer Overflow</h3>
<p>When a local buffer is overflowed on the stack, the attacker can overwrite the
saved return address, redirecting program execution — this is the classic <b>stack smashing</b> attack.</p>

<h3>Heap Buffer Overflow</h3>
<p>When a heap buffer is overflowed, adjacent heap metadata or data can be corrupted,
potentially leading to arbitrary code execution.</p>

<h3>Off-by-One Error</h3>
<p>A common variant: writing exactly one byte past the buffer end. Often caused by
using <code>&lt;=</code> instead of <code>&lt;</code> in loop conditions.</p>
""",
        "causes": [
            ("Using unsafe functions", "gets(), strcpy(), sprintf() don't check buffer bounds"),
            ("Incorrect loop bounds", "Using <= instead of <, or wrong size calculation"),
            ("Missing size checks", "Not validating input size before copying"),
            ("Integer overflow in size calc", "Size calculation overflows, resulting in too-small buffer"),
        ],
        "code_examples": [
            {
                "title": "Classic gets() Buffer Overflow",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdio.h&gt;</span>

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">char</span> <span style="color:#f59e0b;">buffer</span>[<span style="color:#06b6d4;">16</span>];
    
    <span style="color:#6b7280;">// 💥 DANGEROUS: gets() has NO length check</span>
    <span style="color:#6b7280;">// If input > 15 chars, it overflows!</span>
    <span style="color:#22c55e;">gets</span>(<span style="color:#f59e0b;">buffer</span>);
    
    <span style="color:#6b7280;">// ✅ Safe alternative:</span>
    <span style="color:#22c55e;">fgets</span>(<span style="color:#f59e0b;">buffer</span>, <span style="color:#7c3aed;">sizeof</span>(<span style="color:#f59e0b;">buffer</span>), <span style="color:#f59e0b;">stdin</span>);
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ gets() was removed from C11 because it's unfixable. Always use fgets() or getline().</p>""",
            },
            {
                "title": "Off-by-One Error",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;string.h&gt;</span>

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">char</span> <span style="color:#f59e0b;">dst</span>[<span style="color:#06b6d4;">8</span>];
    <span style="color:#7c3aed;">const char</span> <span style="color:#f59e0b;">*src</span> = <span style="color:#06b6d4;">"Hello!!"</span>;  <span style="color:#6b7280;">// 7 chars + null = 8 bytes</span>
    
    <span style="color:#6b7280;">// 💥 Off-by-one: copies 8 bytes but dst[7] should be '\\0'</span>
    <span style="color:#6b7280;">// and we need room for the null terminator</span>
    <span style="color:#7c3aed;">for</span> (<span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">i</span> = <span style="color:#06b6d4;">0</span>; <span style="color:#f59e0b;">i</span> <= <span style="color:#06b6d4;">7</span>; <span style="color:#f59e0b;">i</span>++) {
        <span style="color:#f59e0b;">dst</span>[<span style="color:#f59e0b;">i</span>] = <span style="color:#f59e0b;">src</span>[<span style="color:#f59e0b;">i</span>]; <span style="color:#6b7280;">// When i=7, writes null</span>
    }
    <span style="color:#6b7280;">// If src was 8+ chars, we'd overflow</span>
    
    <span style="color:#6b7280;">// ✅ Safe: use strncpy with proper size</span>
    <span style="color:#22c55e;">strncpy</span>(<span style="color:#f59e0b;">dst</span>, <span style="color:#f59e0b;">src</span>, <span style="color:#7c3aed;">sizeof</span>(<span style="color:#f59e0b;">dst</span>) - <span style="color:#06b6d4;">1</span>);
    <span style="color:#f59e0b;">dst</span>[<span style="color:#7c3aed;">sizeof</span>(<span style="color:#f59e0b;">dst</span>) - <span style="color:#06b6d4;">1</span>] = <span style="color:#06b6d4;">'\\0'</span>;
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ Off-by-one errors are subtle and may not crash immediately, making them hard to find.</p>""",
            },
        ],
        "detection": """
<h3>Detection</h3>
<ul>
<li><b>Stack Canaries</b>: <code>-fstack-protector-all</code> — places a guard value before the return address</li>
<li><b>AddressSanitizer</b>: <code>-fsanitize=address</code> — detects buffer overflows at runtime</li>
<li><b>FORTIFY_SOURCE</b>: <code>-D_FORTIFY_SOURCE=2</code> — replaces unsafe functions with safe versions</li>
<li><b>Valgrind</b>: Detects invalid reads/writes</li>
<li><b>Static analysis</b>: <code>cppcheck</code>, <code>clang-tidy</code>, Coverity</li>
</ul>

<h3>Prevention</h3>
<ol>
<li>Never use <code>gets()</code>, <code>strcpy()</code>, <code>sprintf()</code> — use <code>fgets()</code>, <code>strncpy()</code>, <code>snprintf()</code></li>
<li>Always check buffer sizes before copying</li>
<li>Use <code>sizeof(buffer)</code> instead of hardcoding sizes</li>
<li>Use C++ containers (<code>std::vector</code>, <code>std::string</code>) instead of raw arrays</li>
<li>Compile with <code>-Wall -Wextra -Werror</code></li>
</ol>
""",
        "quiz": {
            "question": "Why was gets() removed from the C standard in C11?",
            "options": [
                "It was too slow",
                "It cannot be used safely — it has no way to limit input length",
                "It didn't support Unicode",
                "It was replaced by scanf()"
            ],
            "correct": 1,
            "explanation": "gets() reads input with NO length limit. It's impossible to use safely because any input longer than the buffer will overflow it. fgets() is the safe replacement."
        }
    },
    "double_free": {
        "title": "Double Free",
        "icon": "🔄",
        "signal": "Undefined Behavior / Crash",
        "summary": "A double free occurs when free() is called more than once on the same memory allocation, potentially corrupting the heap allocator's data structures.",
        "description": """
<h2>What is a Double Free?</h2>
<p>A <b>double free</b> occurs when <code>free()</code> is called on a pointer that has already been freed.
This is <b>undefined behavior</b> in C and can have serious consequences:</p>

<h3>What Happens Internally?</h3>
<p>When you call <code>free(ptr)</code>:</p>
<ol>
<li>The allocator marks the memory block as available</li>
<li>The block may be coalesced with adjacent free blocks</li>
<li>The block's metadata is updated</li>
</ol>
<p>If you call <code>free(ptr)</code> again:</p>
<ol>
<li>The allocator may try to free an already-free block</li>
<li>Heap metadata gets corrupted</li>
<li>This can lead to <b>arbitrary code execution</b> (security vulnerability!)</li>
</ol>

<h3>Security Impact</h3>
<p>Double-free vulnerabilities are a serious security issue. An attacker who can control
the timing of double frees can manipulate heap metadata to achieve arbitrary write
primitives, often leading to full code execution.</p>
""",
        "causes": [
            ("Calling free() twice on same pointer", "The most direct cause — forgetting the pointer was already freed"),
            ("Multiple owners freeing same memory", "Poor ownership semantics — two parts of code think they own the memory"),
            ("Error path frees already-freed memory", "In error handling code, freeing memory that was already freed in normal path"),
            ("Not setting pointer to NULL after free", "Allows the non-NULL pointer to be freed again"),
        ],
        "code_examples": [
            {
                "title": "Basic Double Free",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdlib.h&gt;</span>

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">*data</span> = (<span style="color:#7c3aed;">int</span>*)<span style="color:#22c55e;">malloc</span>(<span style="color:#7c3aed;">sizeof</span>(<span style="color:#7c3aed;">int</span>));
    <span style="color:#f59e0b;">*data</span> = <span style="color:#06b6d4;">42</span>;
    
    <span style="color:#22c55e;">free</span>(<span style="color:#f59e0b;">data</span>);   <span style="color:#6b7280;">// First free — OK</span>
    <span style="color:#22c55e;">free</span>(<span style="color:#f59e0b;">data</span>);   <span style="color:#6b7280;">// 💥 Double free — UNDEFINED BEHAVIOR!</span>
    
    <span style="color:#6b7280;">// ✅ Correct: set to NULL after free</span>
    <span style="color:#f59e0b;">data</span> = <span style="color:#ef4444;">NULL</span>;
    <span style="color:#22c55e;">free</span>(<span style="color:#f59e0b;">data</span>);   <span style="color:#6b7280;">// Safe: free(NULL) is a no-op</span>
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ free(NULL) is guaranteed to be safe (does nothing). Always set pointers to NULL after freeing!</p>""",
            },
        ],
        "detection": """
<h3>Detection</h3>
<ul>
<li><b>AddressSanitizer</b>: <code>-fsanitize=address</code> — immediately catches double free</li>
<li><b>Valgrind</b>: Reports "Invalid free() / delete / delete[]"</li>
<li><b>dmalloc</b>: Debug malloc library that catches double frees</li>
<li><b>Electric Fence</b>: Memory debugger that catches various heap errors</li>
</ul>

<h3>Prevention</h3>
<ol>
<li><b>Always set pointers to NULL after free</b> — <code>free(ptr); ptr = NULL;</code></li>
<li>Use RAII patterns in C++ (smart pointers, constructors/destructors)</li>
<li>Clearly define memory ownership — who is responsible for freeing?</li>
<li>Use <code>std::unique_ptr</code> for single ownership, <code>std::shared_ptr</code> for shared</li>
</ol>
""",
        "quiz": {
            "question": "What happens when you call free(NULL)?",
            "options": [
                "It causes a segmentation fault",
                "It is undefined behavior",
                "It does nothing (it's guaranteed to be safe)",
                "It allocates a zero-size block"
            ],
            "correct": 2,
            "explanation": "The C standard explicitly guarantees that free(NULL) is a no-op and does nothing. This is why setting pointers to NULL after free is a useful pattern."
        }
    },
    "memory_leak": {
        "title": "Memory Leak",
        "icon": "💧",
        "signal": "No signal (gradual degradation)",
        "summary": "A memory leak occurs when dynamically allocated memory is never freed, causing the program's memory usage to grow over time until the system runs out of memory.",
        "description": """
<h2>What is a Memory Leak?</h2>
<p>A <b>memory leak</b> occurs when a program allocates memory dynamically (using <code>malloc()</code>,
<code>new</code>, etc.) but never releases it with <code>free()</code> or <code>delete</code>.
The memory remains allocated but unreachable.</p>

<h3>Types of Memory Leaks</h3>
<ul>
<li><b>Direct leak</b>: Pointer to allocated memory is lost (goes out of scope, overwritten)</li>
<li><b>Indirect leak</b>: Memory is reachable only through another leaked pointer</li>
<li><b>Still reachable</b>: Memory is still reachable at program exit (often not a true leak)</li>
</ul>

<h3>Impact</h3>
<p>Short-running programs: usually harmless (OS reclaims all memory at exit).<br>
Long-running programs (servers, daemons): <b>critical</b> — the program eventually
consumes all available memory and the OOM killer terminates it.</p>

<h3>Real-World Impact</h3>
<p>Memory leaks have caused major outages in production systems. Even small leaks
accumulate over time in long-running processes.</p>
""",
        "causes": [
            ("Lost pointer", "Overwriting a pointer before freeing the memory it points to"),
            ("Missing free/delete", "Simply forgetting to deallocate memory"),
            ("Exception before free", "An exception/error path skips the free() call"),
            ("Reassignment without free", "Reassigning a pointer without freeing the old memory"),
            ("Circular references", "In reference-counted systems, circular refs prevent deallocation"),
        ],
        "code_examples": [
            {
                "title": "Basic Memory Leak",
                "language": "C",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdlib.h&gt;</span>

<span style="color:#7c3aed;">void</span> <span style="color:#22c55e;">leak_memory</span>() {
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">*data</span> = (<span style="color:#7c3aed;">int</span>*)<span style="color:#22c55e;">malloc</span>(<span style="color:#06b6d4;">1000</span> * <span style="color:#7c3aed;">sizeof</span>(<span style="color:#7c3aed;">int</span>));
    <span style="color:#f59e0b;">*data</span> = <span style="color:#06b6d4;">42</span>;
    <span style="color:#6b7280;">// 💥 Function returns without free(data)</span>
    <span style="color:#6b7280;">// 4000 bytes are now leaked!</span>
}

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">for</span> (<span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">i</span> = <span style="color:#06b6d4;">0</span>; <span style="color:#f59e0b;">i</span> &lt; <span style="color:#06b6d4;">1000000</span>; <span style="color:#f59e0b;">i</span>++) {
        <span style="color:#22c55e;">leak_memory</span>();  <span style="color:#6b7280;">// Leaks 4GB!</span>
    }
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ Each call leaks 4000 bytes. A million calls = ~4 GB leaked. Long-running programs will eventually crash.</p>""",
            },
            {
                "title": "C++ Memory Leak with Exceptions",
                "language": "C++",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;stdexcept&gt;</span>

<span style="color:#7c3aed;">void</span> <span style="color:#22c55e;">process</span>() {
    <span style="color:#7c3aed;">int</span>* <span style="color:#f59e0b;">data</span> = <span style="color:#7c3aed;">new</span> <span style="color:#7c3aed;">int</span>[<span style="color:#06b6d4;">1000</span>];
    
    <span style="color:#7c3aed;">if</span> (<span style="color:#06b6d4;">true</span>) {
        <span style="color:#7c3aed;">throw</span> <span style="color:#06b6d4;">std::runtime_error</span>(<span style="color:#06b6d4;">"Error!"</span>);
    }
    <span style="color:#6b7280;">// 💥 Never reached! Memory leaked.</span>
    <span style="color:#7c3aed;">delete</span>[] <span style="color:#f59e0b;">data</span>;
}

<span style="color:#6b7280;">// ✅ Correct: use smart pointers</span>
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;memory&gt;</span>
<span style="color:#7c3aed;">void</span> <span style="color:#22c55e;">process_safe</span>() {
    <span style="color:#7c3aed;">auto</span> <span style="color:#f59e0b;">data</span> = <span style="color:#06b6d4;">std::make_unique</span>&lt;<span style="color:#7c3aed;">int</span>[]&gt;(<span style="color:#06b6d4;">1000</span>);
    <span style="color:#7c3aed;">if</span> (<span style="color:#06b6d4;">true</span>) {
        <span style="color:#7c3aed;">throw</span> <span style="color:#06b6d4;">std::runtime_error</span>(<span style="color:#06b6d4;">"Error!"</span>);
    }
    <span style="color:#6b7280;">// data is automatically freed when exception propagates</span>
}</pre>
<p style="color:#f87171;">⚠️ Exceptions bypass normal control flow. Use RAII (smart pointers) to guarantee cleanup.</p>""",
            },
        ],
        "detection": """
<h3>Detection</h3>
<ul>
<li><b>Valgrind</b>: <code>valgrind --leak-check=full --show-leak-kinds=all ./program</code></li>
<li><b>AddressSanitizer</b>: <code>-fsanitize=address</code> with <code>ASAN_OPTIONS=detect_leaks=1</code></li>
<li><b>LeakSanitizer</b>: Standalone leak detector (LSan)</li>
<li><b>Heob</b>: Heap observer for Windows</li>
<li><b>Visual Studio CRT Debug Heap</b>: Built-in leak detection on Windows</li>
</ul>

<h3>Prevention</h3>
<ol>
<li>Use RAII — every resource has a owning object that releases it in the destructor</li>
<li>Use <code>std::unique_ptr</code> and <code>std::shared_ptr</code> instead of raw <code>new</code>/<code>delete</code></li>
<li>Use STL containers (<code>std::vector</code>, <code>std::string</code>) instead of raw arrays</li>
<li>Follow the "one function allocates, one function frees" rule</li>
<li>Run leak checks regularly during development</li>
</ol>
""",
        "quiz": {
            "question": "Why are memory leaks particularly dangerous in long-running programs like servers?",
            "options": [
                "They make compilation slower",
                "The leaked memory accumulates over time, eventually exhausting available memory",
                "They cause immediate crashes",
                "They only affect the stack"
            ],
            "correct": 1,
            "explanation": "In long-running processes, even tiny leaks (a few bytes per request) accumulate over days/weeks/months until the process consumes all available RAM, leading to OOM kills or system instability."
        }
    },
    "use_after_free": {
        "title": "Use After Free",
        "icon": "👻",
        "signal": "Undefined Behavior / SIGSEGV",
        "summary": "A use-after-free (UAF) occurs when a program continues to use a pointer after the memory it points to has been freed, leading to undefined behavior and potential security exploits.",
        "description": """
<h2>What is Use After Free?</h2>
<p><b>Use-after-free</b> (UAF) is a class of vulnerability where a program dereferences a pointer
after the memory it points to has been freed. The behavior is <b>undefined</b>:</p>
<ul>
<li>The program might crash (segfault)</li>
<li>The program might appear to work correctly (if memory hasn't been reused)</li>
<li>The program might produce wrong results (if memory has been reused)</li>
<li>An attacker might exploit it for code execution</li>
</ul>

<h3>Why It's Dangerous</h3>
<p>UAF is one of the most exploited vulnerability classes. Attackers can:</p>
<ol>
<li>Free the memory</li>
<li>Trigger allocation of a different object at the same address</li>
<li>Access the old pointer, now pointing to the new object</li>
<li>This creates a <b>type confusion</b> enabling data manipulation</li>
</ol>

<h3>Common in C++</h3>
<p>UAF is especially common in C++ with:</p>
<ul>
<li>Raw pointers stored in containers</li>
<li>Observers accessing destroyed subjects</li>
<li>Callbacks capturing <code>this</code> of destroyed objects</li>
</ul>
""",
        "causes": [
            ("Dereferencing after free", "Using a pointer after calling free() on it"),
            ("Accessing destroyed C++ object", "Calling methods on a deleted object"),
            ("Stale reference in callback", "Callback captures pointer to object that was later destroyed"),
            ("Race condition", "One thread frees while another thread uses the pointer"),
        ],
        "code_examples": [
            {
                "title": "Use After Free in C++",
                "language": "C++",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;iostream&gt;</span>

<span style="color:#7c3aed;">class</span> <span style="color:#22c55e;">Widget</span> {
<span style="color:#7c3aed;">public:</span>
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">value</span>;
    <span style="color:#22c55e;">Widget</span>(<span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">v</span>) : <span style="color:#f59e0b;">value</span>(<span style="color:#f59e0b;">v</span>) {}
    <span style="color:#7c3aed;">void</span> <span style="color:#22c55e;">print</span>() { <span style="color:#06b6d4;">std::cout</span> &lt;&lt; <span style="color:#f59e0b;">value</span>; }
};

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#22c55e;">Widget</span>* <span style="color:#f59e0b;">w</span> = <span style="color:#7c3aed;">new</span> <span style="color:#22c55e;">Widget</span>(<span style="color:#06b6d4;">42</span>);
    
    <span style="color:#7c3aed;">delete</span> <span style="color:#f59e0b;">w</span>;  <span style="color:#6b7280;">// Memory freed</span>
    
    <span style="color:#6b7280;">// 💥 Use After Free: calling method on deleted object</span>
    <span style="color:#f59e0b;">w</span>-&gt;<span style="color:#22c55e;">print</span>();  <span style="color:#6b7280;">// Undefined behavior!</span>
    
    <span style="color:#6b7280;">// Might work, might crash, might print garbage</span>
    
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ The most dangerous aspect: it MIGHT work sometimes, hiding the bug until it causes a critical failure.</p>""",
            },
        ],
        "detection": """
<h3>Detection</h3>
<ul>
<li><b>AddressSanitizer</b>: <code>-fsanitize=address</code> — catches UAF with high accuracy</li>
<li><b>Valgrind/Memcheck</b>: Reports "Invalid read/write" after free</li>
<li><b>CFFI Sanitizer</b>: Specialized for UAF in browsers</li>
<li><b>MProtect-based tools</b>: Mark freed pages as inaccessible</li>
</ul>

<h3>Prevention</h3>
<ol>
<li>Set pointers to <code>NULL</code> immediately after <code>free()</code>/<code>delete</code></li>
<li>Use C++ smart pointers: <code>std::unique_ptr</code>, <code>std::shared_ptr</code></li>
<li>Use <code>std::weak_ptr</code> to break circular references and observe without owning</li>
<li>Implement clear ownership semantics</li>
<li>Use after-free hardening: <code>ASAN_OPTIONS=quarantine_size=256M</code></li>
</ol>
""",
        "quiz": {
            "question": "Why is use-after-free particularly dangerous as a security vulnerability?",
            "options": [
                "It always causes an immediate crash",
                "The freed memory can be reallocated with a different type, creating type confusion that attackers can exploit",
                "It only affects the stack",
                "It can only happen in C, not C++"
            ],
            "correct": 1,
            "explanation": "After free(), the allocator may reuse that memory for a different object. If the old (dangling) pointer is then used, it accesses the new object as if it were the old type — this 'type confusion' enables sophisticated exploits."
        }
    },
    "dangling_pointer": {
        "title": "Dangling Pointer",
        "icon": "🔗",
        "signal": "SIGSEGV / Undefined Behavior",
        "summary": "A dangling pointer points to memory that has been freed or has gone out of scope. Dereferencing it leads to undefined behavior.",
        "description": """
<h2>What is a Dangling Pointer?</h2>
<p>A <b>dangling pointer</b> is a pointer that still holds the address of memory that
has been deallocated or has gone out of scope. The pointer "dangles" — it points
to something that no longer exists.</p>

<h3>Common Scenarios</h3>
<ol>
<li><b>Stack dangling pointer</b>: Pointer to a local variable that went out of scope</li>
<li><b>Heap dangling pointer</b>: Pointer to memory that has been freed</li>
<li><b>Object dangling pointer</b>: Pointer to a destroyed C++ object</li>
</ol>

<h3>Dangling vs Wild Pointer</h3>
<ul>
<li><b>Dangling pointer</b>: Was valid at some point, now invalid</li>
<li><b>Wild pointer</b>: Never initialized, contains garbage address</li>
</ul>

<h3>Dangling Reference in C++</h3>
<p>C++ references can also dangle — this is even more dangerous because
references can't be NULL, giving a false sense of safety.</p>
""",
        "causes": [
            ("Returning reference to local", "Returning a reference to a stack variable that's destroyed"),
            ("Pointer to freed memory", "Not nullifying a pointer after free()"),
            ("Reference to temporary", "Binding a reference to a temporary that's destroyed"),
            ("Iterator invalidation", "Using an iterator after the container is modified"),
        ],
        "code_examples": [
            {
                "title": "Dangling Reference in C++",
                "language": "C++",
                "code": """<pre style="color:#e2e8f0; background:#0d0e1a; padding:16px; border-radius:8px; font-family:'Cascadia Code','Fira Code',monospace; font-size:13px; overflow-x:auto;">
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;iostream&gt;</span>
<span style="color:#7c3aed;">#include</span> <span style="color:#06b6d4;">&lt;vector&gt;</span>

<span style="color:#6b7280;">// 💥 Dangling reference to local variable</span>
<span style="color:#7c3aed;">const</span> <span style="color:#7c3aed;">int</span>&amp; <span style="color:#22c55e;">get_value</span>() {
    <span style="color:#7c3aed;">int</span> <span style="color:#f59e0b;">local</span> = <span style="color:#06b6d4;">42</span>;
    <span style="color:#7c3aed;">return</span> <span style="color:#f59e0b;">local</span>;  <span style="color:#6b7280;">// Reference to local destroyed!</span>
}

<span style="color:#6b7280;">// 💥 Iterator invalidation</span>
<span style="color:#7c3aed;">void</span> <span style="color:#22c55e;">bad_iterator</span>() {
    <span style="color:#06b6d4;">std::vector</span>&lt;<span style="color:#7c3aed;">int</span>&gt; <span style="color:#f59e0b;">vec</span> = {<span style="color:#06b6d4;">1</span>, <span style="color:#06b6d4;">2</span>, <span style="color:#06b6d4;">3</span>};
    <span style="color:#7c3aed;">auto</span> <span style="color:#f59e0b;">it</span> = <span style="color:#f59e0b;">vec</span>.<span style="color:#22c55e;">begin</span>();
    <span style="color:#f59e0b;">vec</span>.<span style="color:#22c55e;">push_back</span>(<span style="color:#06b6d4;">4</span>);  <span style="color:#6b7280;">// May reallocate!</span>
    <span style="color:#6b7280;">// 💥 'it' is now dangling — vec may have moved</span>
    <span style="color:#06b6d4;">std::cout</span> &lt;&lt; <span style="color:#f59e0b;">*it</span>;  <span style="color:#6b7280;">// Undefined behavior!</span>
}

<span style="color:#7c3aed;">int</span> <span style="color:#22c55e;">main</span>() {
    <span style="color:#7c3aed;">const</span> <span style="color:#7c3aed;">int</span>&amp; <span style="color:#f59e0b;">ref</span> = <span style="color:#22c55e;">get_value</span>();
    <span style="color:#06b6d4;">std::cout</span> &lt;&lt; <span style="color:#f59e0b;">ref</span>;  <span style="color:#6b7280;">// Undefined behavior!</span>
    <span style="color:#7c3aed;">return</span> <span style="color:#06b6d4;">0</span>;
}</pre>
<p style="color:#f87171;">⚠️ Returning a reference to a local variable is one of the most common dangling pointer bugs.</p>""",
            },
        ],
        "detection": """
<h3>Detection</h3>
<ul>
<li><b>AddressSanitizer</b>: Detects access to freed/invalid memory</li>
<li><b>Valgrind</b>: Reports invalid reads/writes</li>
<li><b>Static analyzers</b>: <code>clang-tidy</code>, <code>cppcheck</code> can detect some cases</li>
<li><b>Compiler warnings</b>: <code>-Wreturn-local-addr</code> (GCC/Clang)</li>
</ul>

<h3>Prevention</h3>
<ol>
<li>Never return references/pointers to local variables</li>
<li>Return by value instead (modern C++ optimizes away copies with RVO/NRVO)</li>
<li>Set pointers to <code>NULL</code>/<code>nullptr</code> after free/delete</li>
<li>Be aware of iterator invalidation rules for each container</li>
<li>Use <code>std::reference_wrapper</code> or smart pointers with clear lifetimes</li>
</ol>
""",
        "quiz": {
            "question": "What is the difference between a dangling pointer and a wild pointer?",
            "options": [
                "They are the same thing",
                "A dangling pointer was once valid; a wild pointer was never initialized",
                "A wild pointer points to freed memory; a dangling pointer points to random memory",
                "Wild pointers only occur in C++; dangling pointers only in C"
            ],
            "correct": 1,
            "explanation": "A dangling pointer held a valid address at some point but the memory was later freed/deallocated. A wild pointer was never initialized and contains an arbitrary garbage address."
        }
    },
}


# ─── Memory Layout Visualization Widget ──────────────────────────────────────

class MemoryLayoutWidget(QWidget):
    """Custom widget that draws a visual representation of process memory layout."""

    def __init__(self, highlight_section=None, parent=None):
        super().__init__(parent)
        self.highlight_section = highlight_section
        self.setMinimumSize(300, 500)
        self.setMaximumWidth(350)

    def set_highlight(self, section):
        self.highlight_section = section
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        margin = 20
        section_w = w - 2 * margin
        total_h = h - 2 * margin

        sections = [
            ("Kernel Space", "#ef4444", "Inaccessible", True),
            ("Stack ↓", "#7c3aed", "Grows downward", False),
            ("↕ Free Space ↕", "#1e1f36", "Available", False),
            ("Heap ↑", "#06b6d4", "Grows upward", False),
            ("BSS", "#f59e0b", "Uninitialized globals", False),
            ("Data", "#22c55e", "Initialized globals", False),
            ("Text (Code)", "#ec4899", "Read + Execute", True),
        ]

        num_sections = len(sections)
        section_h = total_h / num_sections

        # Title
        painter.setPen(QColor("#e2e8f0"))
        font = QFont("Segoe UI", 11, QFont.Bold)
        painter.setFont(font)
        painter.drawText(QRectF(0, 2, w, 18), Qt.AlignCenter, "Virtual Memory Layout")

        y = margin + 20

        # Draw address labels
        painter.setFont(QFont("Cascadia Code", 8))
        painter.setPen(QColor("#6b7280"))

        for i, (name, color, desc, restricted) in enumerate(sections):
            rect = QRectF(margin, y + i * section_h, section_w, section_h - 3)

            # Background
            bg_color = QColor(color)
            is_highlighted = (self.highlight_section and name.lower().startswith(self.highlight_section.lower()))

            if is_highlighted:
                bg_color.setAlpha(180)
                # Draw glow effect
                glow_path = QPainterPath()
                glow_path.addRoundedRect(rect.adjusted(-4, -4, 4, 4), 10, 10)
                painter.fillPath(glow_path, QColor(color + "40"))
            else:
                bg_color.setAlpha(80)

            path = QPainterPath()
            path.addRoundedRect(rect, 8, 8)
            painter.fillPath(path, bg_color)

            # Border
            border_color = QColor(color)
            if is_highlighted:
                border_color.setAlpha(255)
                painter.setPen(QPen(border_color, 3))
            else:
                border_color.setAlpha(120)
                painter.setPen(QPen(border_color, 1))
            painter.drawPath(path)

            # Section name
            text_color = QColor("#ffffff") if is_highlighted else QColor("#e2e8f0")
            painter.setPen(text_color)
            font.setBold(True)
            font.setPointSize(10 if is_highlighted else 9)
            painter.setFont(font)
            painter.drawText(rect.adjusted(10, 4, 0, 0), Qt.AlignLeft | Qt.AlignTop, name)

            # Description
            font.setBold(False)
            font.setPointSize(8)
            painter.setFont(font)
            desc_color = QColor(color) if is_highlighted else QColor("#6b7280")
            painter.setPen(desc_color)
            painter.drawText(rect.adjusted(10, 0, -10, -4), Qt.AlignLeft | Qt.AlignBottom, desc)

            # Restricted icon
            if restricted:
                painter.setPen(QColor("#ef4444"))
                font.setPointSize(10)
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(rect.adjusted(0, 0, -10, 0), Qt.AlignRight | Qt.AlignVCenter, "🔒")

            # Highlight pulse
            if is_highlighted:
                painter.setPen(Qt.NoPen)
                pulse_color = QColor(color)
                pulse_color.setAlpha(30)
                painter.fillPath(path, pulse_color)

        # Address labels on the side
        painter.setFont(QFont("Cascadia Code", 7))
        painter.setPen(QColor("#4a4d7a"))
        addresses = ["0xFFFFFFFF", "0xFFFF...", "0x7FFF...", "", "0x5555...", "0x5555...", "0x400000"]
        for i, addr in enumerate(addresses):
            if addr:
                rect = QRectF(margin - 5, y + i * section_h, section_w + 10, section_h - 3)
                painter.drawText(rect.adjusted(0, 4, 0, 0), Qt.AlignRight | Qt.AlignTop, addr)

        painter.end()


# ─── Interactive Memory Simulator Widget ──────────────────────────────────────

class MemorySimulator(QWidget):
    """Interactive widget that simulates a simple memory model for educational purposes."""

    operation_result = Signal(str, str)  # message, type (success/error/warning)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.memory = {}  # address -> (value, allocated, name)
        self.next_addr = 1000
        self.freed_addrs = set()
        self.allocated_names = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Title
        title = QLabel("🎮 Interactive Memory Simulator")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #7c3aed;")
        layout.addWidget(title)

        # Memory grid display
        self.grid_frame = QFrame()
        self.grid_frame.setStyleSheet("""
            QFrame {
                background-color: #12132a;
                border: 1px solid #2d2f52;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        self.grid_layout = QGridLayout(self.grid_frame)
        self.grid_layout.setSpacing(3)

        # Initialize memory grid (8x8 = 64 cells)
        self.cells = []
        for i in range(64):
            addr = 1000 + i * 4
            self.memory[addr] = (0, False, None)
            label = QLabel("—")
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(36, 28)
            label.setStyleSheet("""
                QLabel {
                    background-color: #1a1b2e;
                    border: 1px solid #2d2f52;
                    border-radius: 3px;
                    font-family: 'Cascadia Code';
                    font-size: 10px;
                    color: #4a4d7a;
                }
            """)
            label.setToolTip(f"Address: {addr} (0x{addr:04x})\nStatus: Free")
            row, col = divmod(i, 8)
            self.grid_layout.addWidget(label, row, col)
            self.cells.append(label)

        layout.addWidget(self.grid_frame)

        # Controls
        ctrl_group = QGroupBox("Operations")
        ctrl_layout = QGridLayout(ctrl_group)

        # Allocate
        ctrl_layout.addWidget(QLabel("Variable:"), 0, 0)
        self.name_input = QLabel("var1")
        self.name_input.setStyleSheet("color: #06b6d4; font-family: 'Cascadia Code';")
        self.var_counter = 1
        ctrl_layout.addWidget(self.name_input, 0, 1)

        alloc_btn = QPushButton("📦 Allocate")
        alloc_btn.setObjectName("success")
        alloc_btn.clicked.connect(self._allocate)
        ctrl_layout.addWidget(alloc_btn, 0, 2)

        # Write
        ctrl_layout.addWidget(QLabel("Address:"), 1, 0)
        self.addr_combo = QComboBox()
        self.addr_combo.setStyleSheet("background: #16172b; border: 1px solid #2d2f52; border-radius: 4px; padding: 4px; color: #e2e8f0;")
        ctrl_layout.addWidget(self.addr_combo, 1, 1)

        write_btn = QPushButton("✏️ Write")
        write_btn.clicked.connect(self._write)
        ctrl_layout.addWidget(write_btn, 1, 2)

        # Read
        read_btn = QPushButton("📖 Read")
        read_btn.setObjectName("secondary")
        read_btn.clicked.connect(self._read)
        ctrl_layout.addWidget(read_btn, 2, 0)

        # Free
        free_btn = QPushButton("🗑️ Free")
        free_btn.setObjectName("danger")
        free_btn.clicked.connect(self._free)
        ctrl_layout.addWidget(free_btn, 2, 1)

        # Simulate errors
        err_btn = QPushButton("💥 Simulate Error")
        err_btn.setObjectName("danger")
        err_btn.clicked.connect(self._simulate_error)
        ctrl_layout.addWidget(err_btn, 2, 2)

        layout.addWidget(ctrl_group)

        # Result display
        self.result_label = QLabel("Perform an operation to see results...")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #12132a;
                border: 1px solid #2d2f52;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Cascadia Code';
                font-size: 12px;
                color: #a0a4c8;
                min-height: 60px;
            }
        """)
        layout.addWidget(self.result_label)

    def _update_grid(self):
        for i in range(64):
            addr = 1000 + i * 4
            value, allocated, name = self.memory[addr]
            label = self.cells[i]

            if addr in self.freed_addrs:
                label.setText("💀")
                label.setStyleSheet("""
                    QLabel {
                        background-color: #7f1d1d;
                        border: 1px solid #ef4444;
                        border-radius: 3px;
                        font-size: 12px;
                        color: #fca5a5;
                    }
                """)
                label.setToolTip(f"Address: {addr} (0x{addr:04x})\nStatus: FREED (dangling!)\n⚠️ Accessing this = Use-After-Free!")
            elif allocated:
                label.setText(str(value))
                label.setStyleSheet("""
                    QLabel {
                        background-color: #164e63;
                        border: 1px solid #06b6d4;
                        border-radius: 3px;
                        font-family: 'Cascadia Code';
                        font-size: 10px;
                        color: #67e8f9;
                    }
                """)
                label.setToolTip(f"Address: {addr} (0x{addr:04x})\nName: {name}\nValue: {value}\nStatus: Allocated")
            else:
                label.setText("—")
                label.setStyleSheet("""
                    QLabel {
                        background-color: #1a1b2e;
                        border: 1px solid #2d2f52;
                        border-radius: 3px;
                        font-family: 'Cascadia Code';
                        font-size: 10px;
                        color: #4a4d7a;
                    }
                """)
                label.setToolTip(f"Address: {addr} (0x{addr:04x})\nStatus: Free")

    def _allocate(self):
        # Find contiguous free block of size 4
        for start in range(0, 61, 4):
            all_free = all(not self.memory[1000 + start + j][1] and (1000 + start + j) not in self.freed_addrs for j in range(4))
            if all_free:
                name = f"var{self.var_counter}"
                self.var_counter += 1
                for j in range(4):
                    addr = 1000 + start + j
                    self.memory[addr] = (0, True, name)
                    self.freed_addrs.discard(addr)
                self.allocated_names[name] = 1000 + start
                self.addr_combo.addItem(f"{name} @ {1000+start}", 1000 + start)
                self._update_grid()
                self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #a0a4c8;", "color: #22c55e;"))
                self.result_label.setText(f"✅ Allocated '{name}' at addresses {1000+start}-{1000+start+3}\nmalloc() returned: 0x{1000+start:04x}")
                return
        self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #a0a4c8;", "color: #f59e0b;"))
        self.result_label.setText("⚠️ Out of memory! No free blocks available.")

    def _write(self):
        idx = self.addr_combo.currentIndex()
        if idx < 0:
            self.result_label.setText("⚠️ No variable selected")
            return
        addr = self.addr_combo.itemData(idx)
        if addr in self.freed_addrs:
            self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #22c55e;", "color: #ef4444;").replace("color: #a0a4c8;", "color: #ef4444;"))
            self.result_label.setText(
                f"💥 SEGFAULT / USE-AFTER-FREE!\n"
                f"Tried to write to address 0x{addr:04x}\n"
                f"This memory was already freed!\n"
                f"Signal: SIGSEGV (Signal 11)\n"
                f"Result: Program terminated abnormally"
            )
            return
        if not self.memory[addr][1]:
            self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #22c55e;", "color: #ef4444;").replace("color: #a0a4c8;", "color: #ef4444;"))
            self.result_label.setText(
                f"💥 SEGFAULT!\n"
                f"Tried to write to address 0x{addr:04x}\n"
                f"This memory was never allocated!\n"
                f"Signal: SIGSEGV (Signal 11)"
            )
            return
        value, allocated, name = self.memory[addr]
        import random
        new_val = random.randint(1, 99)
        self.memory[addr] = (new_val, True, name)
        self._update_grid()
        self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #ef4444;", "color: #22c55e;").replace("color: #a0a4c8;", "color: #22c55e;"))
        self.result_label.setText(f"✅ Wrote value {new_val} to '{name}' at 0x{addr:04x}")

    def _read(self):
        idx = self.addr_combo.currentIndex()
        if idx < 0:
            self.result_label.setText("⚠️ No variable selected")
            return
        addr = self.addr_combo.itemData(idx)
        if addr in self.freed_addrs:
            self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #22c55e;", "color: #ef4444;").replace("color: #a0a4c8;", "color: #ef4444;"))
            self.result_label.setText(
                f"💥 USE-AFTER-FREE!\n"
                f"Tried to read from freed address 0x{addr:04x}\n"
                f"Undefined behavior — could read garbage, crash, or appear to work\n"
                f"Signal: Possibly SIGSEGV"
            )
            return
        if not self.memory[addr][1]:
            self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #22c55e;", "color: #ef4444;").replace("color: #a0a4c8;", "color: #ef4444;"))
            self.result_label.setText(
                f"💥 SEGFAULT!\n"
                f"Tried to read from unallocated address 0x{addr:04x}\n"
                f"Signal: SIGSEGV (Signal 11)"
            )
            return
        value, allocated, name = self.memory[addr]
        self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #ef4444;", "color: #22c55e;").replace("color: #a0a4c8;", "color: #22c55e;"))
        self.result_label.setText(f"✅ Read value {value} from '{name}' at 0x{addr:04x}")

    def _free(self):
        idx = self.addr_combo.currentIndex()
        if idx < 0:
            self.result_label.setText("⚠️ No variable selected")
            return
        addr = self.addr_combo.itemData(idx)
        name = self.memory[addr][2]

        if addr in self.freed_addrs:
            self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #22c55e;", "color: #ef4444;").replace("color: #a0a4c8;", "color: #ef4444;"))
            self.result_label.setText(
                f"💥 DOUBLE FREE!\n"
                f"Tried to free address 0x{addr:04x} ('{name}') again!\n"
                f"free() was already called on this pointer.\n"
                f"Result: Heap corruption — undefined behavior\n"
                f"This is a critical security vulnerability!"
            )
            return

        if not self.memory[addr][1]:
            self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #22c55e;", "color: #ef4444;").replace("color: #a0a4c8;", "color: #ef4444;"))
            self.result_label.setText(
                f"💥 INVALID FREE!\n"
                f"Tried to free address 0x{addr:04x} which was never allocated!\n"
                f"Result: Undefined behavior — likely crash"
            )
            return

        # Mark all cells of this variable as freed
        for a in range(64):
            real_addr = 1000 + a
            if self.memory[real_addr][2] == name and self.memory[real_addr][1]:
                self.memory[real_addr] = (self.memory[real_addr][0], True, name)
                self.freed_addrs.add(real_addr)

        self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #ef4444;", "color: #f59e0b;").replace("color: #a0a4c8;", "color: #f59e0b;"))
        self.result_label.setText(
            f"⚠️ Freed '{name}' at 0x{addr:04x}\n"
            f"Memory is now marked as freed (💀 in grid)\n"
            f"⚠️ The pointer still holds this address — it's now DANGLING!\n"
            f"Try reading or writing to see use-after-free in action!"
        )
        self._update_grid()

    def _simulate_error(self):
        # Create an interesting scenario
        self.result_label.setStyleSheet(self.result_label.styleSheet().replace("color: #22c55e;", "color: #06b6d4;").replace("color: #ef4444;", "color: #06b6d4;").replace("color: #a0a4c8;", "color: #06b6d4;"))
        self.result_label.setText(
            "💡 Error Simulation Scenarios:\n\n"
            "1. SEGFAULT: Allocate → Free → Read (use-after-free)\n"
            "2. DOUBLE FREE: Allocate → Free → Free again\n"
            "3. NULL DEREF: Try to read from unallocated address\n"
            "4. BUFFER OVERFLOW: Allocate, then try writing beyond bounds\n\n"
            "Try these operations step by step to see what happens!"
        )


# ─── Quiz Widget ──────────────────────────────────────────────────────────────

class QuizWidget(QWidget):
    """Interactive quiz widget for testing knowledge."""

    quiz_completed = Signal(bool, int, int)  # passed, correct, total

    def __init__(self, quiz_data, parent=None):
        super().__init__(parent)
        self.quiz_data = quiz_data
        self.selected_answer = -1
        self.answered = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # Question
        q_label = QLabel(f"❓ {self.quiz_data['question']}")
        q_label.setWordWrap(True)
        q_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #e2e8f0; padding: 8px;")
        layout.addWidget(q_label)

        # Options
        self.button_group = QButtonGroup(self)
        self.radio_buttons = []

        for i, option in enumerate(self.quiz_data["options"]):
            rb = QRadioButton(option)
            rb.setStyleSheet("font-size: 13px; padding: 6px;")
            self.button_group.addButton(rb, i)
            self.radio_buttons.append(rb)
            layout.addWidget(rb)

        self.button_group.idClicked.connect(self._on_option_selected)

        # Submit button
        self.submit_btn = QPushButton("Submit Answer")
        self.submit_btn.setEnabled(False)
        self.submit_btn.clicked.connect(self._submit)
        layout.addWidget(self.submit_btn)

        # Result
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("font-size: 13px; padding: 12px; border-radius: 8px;")
        self.result_label.hide()
        layout.addWidget(self.result_label)

        layout.addStretch()

    def _on_option_selected(self, btn_id):
        self.selected_answer = btn_id
        self.submit_btn.setEnabled(True)

    def _submit(self):
        if self.selected_answer < 0 or self.answered:
            return

        self.answered = True
        correct = self.quiz_data["correct"]
        is_correct = self.selected_answer == correct

        # Highlight correct/wrong answers
        for i, rb in enumerate(self.radio_buttons):
            rb.setEnabled(False)
            if i == correct:
                rb.setStyleSheet("""
                    QRadioButton { font-size: 13px; padding: 6px; color: #22c55e; font-weight: bold; }
                    QRadioButton::indicator { border-color: #22c55e; background-color: #22c55e; }
                """)
            elif i == self.selected_answer and not is_correct:
                rb.setStyleSheet("""
                    QRadioButton { font-size: 13px; padding: 6px; color: #ef4444; font-weight: bold; }
                    QRadioButton::indicator { border-color: #ef4444; background-color: #ef4444; }
                """)

        if is_correct:
            self.result_label.setStyleSheet("""
                QLabel {
                    background-color: #052e16;
                    border: 1px solid #22c55e;
                    border-radius: 8px;
                    color: #86efac;
                    font-size: 13px;
                    padding: 12px;
                }
            """)
            self.result_label.setText(f"✅ Correct!\n\n{self.quiz_data['explanation']}")
        else:
            self.result_label.setStyleSheet("""
                QLabel {
                    background-color: #450a0a;
                    border: 1px solid #ef4444;
                    border-radius: 8px;
                    color: #fca5a5;
                    font-size: 13px;
                    padding: 12px;
                }
            """)
            self.result_label.setText(f"❌ Incorrect.\n\n{self.quiz_data['explanation']}")

        self.result_label.show()
        self.submit_btn.setText("Already Answered")
        self.submit_btn.setEnabled(False)

        self.quiz_completed.emit(is_correct, 1 if is_correct else 0, 1)


# ─── Error Page Widget ───────────────────────────────────────────────────────

class ErrorPageWidget(QWidget):
    """Page widget for a specific memory error type."""

    def __init__(self, error_key, parent=None):
        super().__init__(parent)
        self.error_key = error_key
        self.data = ERROR_DATA[error_key]
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(16, 16, 16, 16)

        # Header
        header_layout = QHBoxLayout()

        icon_label = QLabel(self.data["icon"])
        icon_label.setStyleSheet("font-size: 36px;")
        header_layout.addWidget(icon_label)

        title_layout = QVBoxLayout()
        title_label = QLabel(self.data["title"])
        title_label.setObjectName("title")
        title_layout.addWidget(title_label)

        if self.data.get("signal"):
            signal_label = QLabel(f"  {self.data['signal']}  ")
            signal_label.setObjectName("signal_badge")
            signal_label.setStyleSheet("""
                background-color: #dc2626;
                color: white;
                border-radius: 4px;
                padding: 3px 10px;
                font-weight: bold;
                font-size: 12px;
                font-family: 'Cascadia Code';
            """)
            title_layout.addWidget(signal_label)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Summary
        summary = QLabel(self.data["summary"])
        summary.setWordWrap(True)
        summary.setStyleSheet("font-size: 14px; color: #a0a4c8; padding: 8px 0px; border-bottom: 1px solid #2d2f52; margin-bottom: 8px;")
        layout.addWidget(summary)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #2d2f52; border-radius: 8px; }
            QTabBar::tab { min-width: 100px; }
        """)

        # Overview tab
        overview_widget = QWidget()
        overview_layout = QHBoxLayout(overview_widget)
        desc_browser = QTextBrowser()
        desc_browser.setOpenExternalLinks(True)
        desc_browser.setHtml(self.data["description"])
        desc_browser.setStyleSheet("background: #12132a; border: none; border-radius: 8px; padding: 12px;")
        overview_layout.addWidget(desc_browser, 2)

        # Memory layout visualization
        mem_section = None
        if "stack" in self.error_key.lower() or "overflow" in self.error_key.lower():
            mem_section = "Stack"
        elif "heap" in self.error_key.lower():
            mem_section = "Heap"
        elif "buffer" in self.error_key.lower():
            mem_section = "Stack"

        mem_viz = MemoryLayoutWidget(highlight_section=mem_section)
        overview_layout.addWidget(mem_viz, 1)

        tabs.addTab(overview_widget, "📖 Overview")

        # Causes tab
        causes_widget = QWidget()
        causes_layout = QVBoxLayout(causes_widget)
        for cause_title, cause_desc in self.data["causes"]:
            cause_group = QGroupBox(cause_title)
            cause_inner = QVBoxLayout(cause_group)
            cause_label = QLabel(cause_desc)
            cause_label.setWordWrap(True)
            cause_label.setStyleSheet("color: #a0a4c8; font-size: 13px;")
            cause_inner.addWidget(cause_label)
            causes_layout.addWidget(cause_group)
        causes_layout.addStretch()
        causes_scroll = QScrollArea()
        causes_scroll.setWidget(causes_widget)
        causes_scroll.setWidgetResizable(True)
        tabs.addTab(causes_scroll, "🔍 Causes")

        # Code Examples tab
        code_widget = QWidget()
        code_layout = QVBoxLayout(code_widget)
        for example in self.data["code_examples"]:
            ex_group = QGroupBox(f"📝 {example['title']} ({example['language']})")
            ex_inner = QVBoxLayout(ex_group)
            code_browser = QTextBrowser()
            code_browser.setHtml(example["code"])
            code_browser.setMaximumHeight(350)
            code_browser.setStyleSheet("background: #0d0e1a; border: none; border-radius: 8px;")
            ex_inner.addWidget(code_browser)
            code_layout.addWidget(ex_group)
        code_layout.addStretch()
        code_scroll = QScrollArea()
        code_scroll.setWidget(code_widget)
        code_scroll.setWidgetResizable(True)
        tabs.addTab(code_scroll, "💻 Code")

        # Detection & Fix tab
        detect_widget = QWidget()
        detect_layout = QHBoxLayout(detect_widget)
        detect_browser = QTextBrowser()
        detect_browser.setOpenExternalLinks(True)
        detect_browser.setHtml(self.data["detection"])
        detect_browser.setStyleSheet("background: #12132a; border: none; border-radius: 8px; padding: 12px;")
        detect_layout.addWidget(detect_browser, 2)

        # Memory simulator
        simulator = MemorySimulator()
        detect_layout.addWidget(simulator, 1)

        detect_scroll = QScrollArea()
        detect_scroll.setWidget(detect_widget)
        detect_scroll.setWidgetResizable(True)
        tabs.addTab(detect_scroll, "🛠️ Detect & Fix")

        # Quiz tab
        quiz_widget = QWidget()
        quiz_layout = QVBoxLayout(quiz_widget)
        quiz_title = QLabel("🧪 Test Your Knowledge")
        quiz_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #7c3aed; padding: 8px;")
        quiz_layout.addWidget(quiz_title)

        quiz = QuizWidget(self.data["quiz"])
        quiz_layout.addWidget(quiz)
        quiz_scroll = QScrollArea()
        quiz_scroll.setWidget(quiz_widget)
        quiz_scroll.setWidgetResizable(True)
        tabs.addTab(quiz_scroll, "🧪 Quiz")

        layout.addWidget(tabs)


# ─── Overview Page Widget ────────────────────────────────────────────────────

class OverviewPageWidget(QWidget):
    """Welcome/overview page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # Hero section
        hero = QLabel("🧠")
        hero.setStyleSheet("font-size: 64px;")
        hero.setAlignment(Qt.AlignCenter)
        layout.addWidget(hero)

        title = QLabel("Memory Error Learning Lab")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #7c3aed;")
        layout.addWidget(title)

        subtitle = QLabel("Master the art of understanding, detecting, and fixing memory errors")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #a0a4c8; margin-bottom: 16px;")
        layout.addWidget(subtitle)

        # Memory layout
        content_layout = QHBoxLayout()

        # Left: description
        desc_browser = QTextBrowser()
        desc_browser.setOpenExternalLinks(True)
        desc_browser.setHtml("""
<h2>Welcome!</h2>
<p>This application will help you understand the most common and dangerous
memory-related errors in C/C++ programming.</p>

<h3>What You'll Learn</h3>
<ul>
<li><b>Segmentation Faults</b> — The most common crash in C/C++ programs</li>
<li><b>Bus Errors</b> — Alignment and hardware-level memory errors</li>
<li><b>Stack Overflows</b> — When the stack grows too deep</li>
<li><b>Buffer Overflows</b> — The most dangerous security vulnerability</li>
<li><b>Double Free</b> — Freeing memory twice</li>
<li><b>Memory Leaks</b> — When memory is allocated but never freed</li>
<li><b>Use After Free</b> — Accessing freed memory</li>
<li><b>Dangling Pointers</b> — Pointers to invalid memory</li>
</ul>

<h3>How to Use This App</h3>
<ol>
<li>Select an error type from the sidebar</li>
<li>Read the <b>Overview</b> to understand the error</li>
<li>Check the <b>Causes</b> to learn what triggers it</li>
<li>Study the <b>Code Examples</b> to see real code</li>
<li>Learn <b>Detection & Fix</b> strategies and try the simulator</li>
<li>Take the <b>Quiz</b> to test your understanding</li>
</ol>

<h3>Key Concepts</h3>
<p>Understanding memory errors requires knowledge of:</p>
<ul>
<li><b>Virtual memory</b> — How the OS maps addresses</li>
<li><b>Memory segments</b> — Text, Data, BSS, Heap, Stack</li>
<li><b>Pointers</b> — Variables that store memory addresses</li>
<li><b>Dynamic allocation</b> — malloc/free, new/delete</li>
<li><b>Stack frames</b> — How function calls use memory</li>
</ul>
""")
        content_layout.addWidget(desc_browser, 2)

        # Right: memory visualization
        mem_viz = MemoryLayoutWidget()
        content_layout.addWidget(mem_viz, 1)

        layout.addLayout(content_layout)

        # Quick reference cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)

        error_types = [
            ("💥", "Segfault", "Accessing\ninvalid memory", "#7c3aed"),
            ("🚌", "Bus Error", "Unaligned\naccess", "#06b6d4"),
            ("📚", "Stack Overflow", "Stack\nexhausted", "#f59e0b"),
            ("📦", "Buffer Overflow", "Writing past\nbuffer bounds", "#ec4899"),
            ("💧", "Memory Leak", "Memory never\nfreed", "#22c55e"),
        ]

        for icon, name, desc, color in error_types:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #1e1f36;
                    border: 2px solid {color};
                    border-radius: 12px;
                    padding: 12px;
                }}
                QFrame:hover {{
                    background-color: #2d2f52;
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(4)
            card_layout.setAlignment(Qt.AlignCenter)

            card_icon = QLabel(icon)
            card_icon.setAlignment(Qt.AlignCenter)
            card_icon.setStyleSheet("font-size: 28px;")
            card_layout.addWidget(card_icon)

            card_name = QLabel(name)
            card_name.setAlignment(Qt.AlignCenter)
            card_name.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {color};")
            card_layout.addWidget(card_name)

            card_desc = QLabel(desc)
            card_desc.setAlignment(Qt.AlignCenter)
            card_desc.setStyleSheet("font-size: 10px; color: #6b7280;")
            card_layout.addWidget(card_desc)

            cards_layout.addWidget(card)

        layout.addLayout(cards_layout)


# ─── Main Window ──────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧠 Memory Error Learning Lab")
        self.setMinimumSize(1100, 750)
        self.resize(1300, 800)
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setMaximumWidth(260)
        sidebar.setMinimumWidth(220)
        sidebar.setStyleSheet("background-color: #16172b; border-right: 2px solid #2d2f52;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(8)
        sidebar_layout.setContentsMargins(8, 16, 8, 16)

        # App logo/title in sidebar
        logo_label = QLabel("🧠 Memory Errors")
        logo_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #7c3aed;
            padding: 8px 12px;
        """)
        sidebar_layout.addWidget(logo_label)

        version_label = QLabel("Learning Lab v1.0")
        version_label.setStyleSheet("font-size: 10px; color: #4a4d7a; padding: 0px 12px 12px 12px; border-bottom: 1px solid #2d2f52;")
        sidebar_layout.addWidget(version_label)

        # Navigation list
        self.nav_list = QListWidget()
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-radius: 8px;
                margin: 2px 4px;
                color: #a0a4c8;
            }
            QListWidget::item:selected {
                background-color: #7c3aed;
                color: #ffffff;
                font-weight: bold;
            }
            QListWidget::item:hover:!selected {
                background-color: #2d2f52;
                color: #e2e8f0;
            }
        """)

        nav_items = [
            ("overview", "🧠 Overview"),
            ("segfault", "💥 Segmentation Fault"),
            ("bus_error", "🚌 Bus Error"),
            ("stack_overflow", "📚 Stack Overflow"),
            ("buffer_overflow", "📦 Buffer Overflow"),
            ("double_free", "🔄 Double Free"),
            ("memory_leak", "💧 Memory Leak"),
            ("use_after_free", "👻 Use After Free"),
            ("dangling_pointer", "🔗 Dangling Pointer"),
        ]

        for key, label in nav_items:
            self.nav_list.addItem(label)

        sidebar_layout.addWidget(self.nav_list)

        # Progress section in sidebar
        progress_label = QLabel("Your Progress")
        progress_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #a0a4c8; padding: 12px 12px 4px 12px; border-top: 1px solid #2d2f52;")
        sidebar_layout.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%v% Complete")
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #2d2f52;
                border-radius: 8px;
                text-align: center;
                background-color: #16172b;
                color: #e2e8f0;
                font-weight: bold;
                height: 20px;
                margin: 4px 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #06b6d4);
                border-radius: 7px;
            }
        """)
        sidebar_layout.addWidget(self.progress_bar)

        self.visited = set()
        sidebar_layout.addStretch()

        # About button
        about_btn = QPushButton("ℹ️ About")
        about_btn.setObjectName("secondary")
        about_btn.clicked.connect(self._show_about)
        sidebar_layout.addWidget(about_btn)

        main_layout.addWidget(sidebar)

        # Content area
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #1a1b2e;")

        # Create all pages
        self.pages = {}

        # Overview page
        overview_page = OverviewPageWidget()
        self.pages["overview"] = overview_page
        self.stack.addWidget(overview_page)

        # Error pages
        error_keys = ["segfault", "bus_error", "stack_overflow", "buffer_overflow",
                       "double_free", "memory_leak", "use_after_free", "dangling_pointer"]

        for key in error_keys:
            page = ErrorPageWidget(key)
            self.pages[key] = page
            self.stack.addWidget(page)

        main_layout.addWidget(self.stack, 1)

        # Status bar
        self.statusBar().setStyleSheet("background-color: #16172b; color: #6b7280; font-size: 11px; border-top: 1px solid #2d2f52;")
        self.statusBar().showMessage("Welcome to Memory Error Learning Lab — Select a topic from the sidebar to begin")

        # Select overview by default
        self.nav_list.setCurrentRow(0)

    def _setup_connections(self):
        self.nav_list.currentRowChanged.connect(self._on_nav_changed)

    def _on_nav_changed(self, row):
        nav_keys = ["overview", "segfault", "bus_error", "stack_overflow",
                     "buffer_overflow", "double_free", "memory_leak",
                     "use_after_free", "dangling_pointer"]

        if 0 <= row < len(nav_keys):
            key = nav_keys[row]
            self.stack.setCurrentWidget(self.pages[key])
            self.visited.add(key)

            # Update progress
            progress = int((len(self.visited) / len(nav_keys)) * 100)
            self.progress_bar.setValue(progress)

            # Update status bar
            data = ERROR_DATA.get(key, {})
            title = data.get("title", "Overview")
            signal = data.get("signal", "")
            if signal:
                self.statusBar().showMessage(f"📚 {title} — Signal: {signal}")
            else:
                self.statusBar().showMessage(f"🏠 {title} — Select a specific error type from the sidebar to learn more")

    def _show_about(self):
        QMessageBox.about(
            self,
            "About Memory Error Learning Lab",
            "<h3>🧠 Memory Error Learning Lab v1.0</h3>"
            "<p>An interactive application for learning about memory-related errors "
            "in C/C++ programming.</p>"
            "<p><b>Covers:</b></p>"
            "<ul>"
            "<li>Segmentation Faults (SIGSEGV)</li>"
            "<li>Bus Errors (SIGBUS)</li>"
            "<li>Stack Overflows</li>"
            "<li>Buffer Overflows</li>"
            "<li>Double Free</li>"
            "<li>Memory Leaks</li>"
            "<li>Use After Free</li>"
            "<li>Dangling Pointers</li>"
            "</ul>"
            "<p>Built with Python and PySide6.</p>"
        )


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set dark palette as base
    from PySide6.QtGui import QPalette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#1a1b2e"))
    palette.setColor(QPalette.WindowText, QColor("#e2e8f0"))
    palette.setColor(QPalette.Base, QColor("#12132a"))
    palette.setColor(QPalette.AlternateBase, QColor("#1e1f36"))
    palette.setColor(QPalette.ToolTipBase, QColor("#2d2f52"))
    palette.setColor(QPalette.ToolTipText, QColor("#e2e8f0"))
    palette.setColor(QPalette.Text, QColor("#e2e8f0"))
    palette.setColor(QPalette.Button, QColor("#2d2f52"))
    palette.setColor(QPalette.ButtonText, QColor("#e2e8f0"))
    palette.setColor(QPalette.BrightText, QColor("#ef4444"))
    palette.setColor(QPalette.Highlight, QColor("#7c3aed"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    # Apply stylesheet
    app.setStyleSheet(DARK_STYLESHEET)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()